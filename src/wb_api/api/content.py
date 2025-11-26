"""Content API for working with product cards."""

from collections.abc import Iterator
from typing import Any

from ..constants import DOMAINS, SANDBOX_DOMAINS
from ..models.content import (
    Category,
    Characteristic,
    CreateCardRequest,
    CreateTagRequest,
    ProductCard,
    ProductCardsResponse,
    Subject,
    TrashRequest,
    UploadMediaRequest,
)
from .base import BaseAPI


class ContentAPI(BaseAPI):
    """API for working with content (product cards)."""

    @property
    def domain(self) -> str:
        """Get domain for Content API."""
        if self._sandbox:
            return SANDBOX_DOMAINS.get("content", DOMAINS["content"])
        return DOMAINS["content"]

    # === Categories and Characteristics ===

    def get_parent_categories(self, locale: str = "ru") -> list[Category]:
        """
        Get list of parent categories.

        Args:
            locale: Locale code (default: "ru")

        Returns:
            List of Category objects
        """
        data = self._get("/content/v2/object/parent/all", params={"locale": locale})
        if not data or "data" not in data:
            return []
        return [Category(**item) for item in data["data"]]

    def get_subjects(
        self,
        name: str | None = None,
        parent_id: int | None = None,
        limit: int = 1000,
        offset: int = 0,
        locale: str = "ru",
    ) -> list[Subject]:
        """
        Get list of subjects (subcategories).

        Args:
            name: Filter by subject name
            parent_id: Filter by parent category ID
            limit: Maximum number of results
            offset: Offset for pagination
            locale: Locale code

        Returns:
            List of Subject objects
        """
        params: dict[str, Any] = {"locale": locale, "limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if parent_id:
            params["parentID"] = parent_id

        data = self._get("/content/v2/object/all", params=params)
        if not data or "data" not in data:
            return []
        return [Subject(**item) for item in data["data"]]

    def get_subject_characteristics(
        self, subject_id: int, locale: str = "ru"
    ) -> list[Characteristic]:
        """
        Get characteristics for a subject.

        Args:
            subject_id: Subject ID
            locale: Locale code

        Returns:
            List of Characteristic objects
        """
        data = self._get(
            f"/content/v2/object/charcs/{subject_id}",
            params={"locale": locale},
        )
        if not data or "data" not in data:
            return []
        return [Characteristic(**item) for item in data["data"]]

    # === Product Cards ===

    def get_cards(
        self,
        limit: int = 100,
        updated_at: str | None = None,
        nm_id: int | None = None,
        text_search: str | None = None,
        with_photo: int = -1,
        locale: str = "ru",
    ) -> ProductCardsResponse:
        """
        Get list of product cards.

        Args:
            limit: Maximum number of cards to return
            updated_at: Filter by update time (for pagination)
            nm_id: Filter by nomenclature ID (for pagination)
            text_search: Search by text
            with_photo: Filter by photo presence (-1: all, 0: without, 1: with)
            locale: Locale code

        Returns:
            ProductCardsResponse object
        """
        body: dict[str, Any] = {
            "settings": {
                "cursor": {"limit": limit},
                "filter": {"withPhoto": with_photo},
            }
        }

        if updated_at and nm_id:
            body["settings"]["cursor"]["updatedAt"] = updated_at
            body["settings"]["cursor"]["nmID"] = nm_id

        if text_search:
            body["settings"]["filter"]["textSearch"] = text_search

        data = self._post("/content/v2/get/cards/list", json=body, params={"locale": locale})
        if not data:
            return ProductCardsResponse(cards=[], cursor={"total": 0})
        return ProductCardsResponse(**data)

    def iter_cards(
        self, batch_size: int = 100, **filters: Any
    ) -> Iterator[ProductCard]:
        """
        Iterator over all product cards with automatic pagination.

        Args:
            batch_size: Number of cards per request
            **filters: Additional filters for get_cards

        Yields:
            ProductCard objects
        """
        updated_at: str | None = None
        nm_id: int | None = None

        while True:
            response = self.get_cards(
                limit=batch_size,
                updated_at=updated_at,
                nm_id=nm_id,
                **filters,
            )

            yield from response.cards

            # Check if there's more data
            if response.cursor.total < batch_size:
                break

            updated_at = response.cursor.updated_at
            nm_id = response.cursor.nm_id

    def create_cards(self, cards: list[CreateCardRequest]) -> dict[str, Any]:
        """
        Create product cards.

        Args:
            cards: List of CreateCardRequest objects

        Returns:
            Response data
        """
        payload = [card.model_dump(by_alias=True) for card in cards]
        return self._post("/content/v2/cards/upload", json=payload)

    def update_cards(self, cards: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Update product cards.

        Args:
            cards: List of card update data

        Returns:
            Response data
        """
        return self._post("/content/v2/cards/update", json=cards)

    def delete_cards(self, nm_ids: list[int]) -> dict[str, Any]:
        """
        Move cards to trash.

        Args:
            nm_ids: List of nomenclature IDs

        Returns:
            Response data
        """
        request = TrashRequest(nm_ids=nm_ids)
        return self._post(
            "/content/v2/cards/delete/trash",
            json=request.model_dump(by_alias=True),
        )

    def recover_cards(self, nm_ids: list[int]) -> dict[str, Any]:
        """
        Recover cards from trash.

        Args:
            nm_ids: List of nomenclature IDs

        Returns:
            Response data
        """
        request = TrashRequest(nm_ids=nm_ids)
        return self._post(
            "/content/v2/cards/recover", json=request.model_dump(by_alias=True)
        )

    # === Media ===

    def upload_media_by_url(
        self, nm_id: int, urls: list[str]
    ) -> dict[str, Any]:
        """
        Upload media files by URLs.

        Args:
            nm_id: Nomenclature ID
            urls: List of media URLs

        Returns:
            Response data
        """
        request = UploadMediaRequest(nm_id=nm_id, data=urls)
        return self._post(
            "/content/v3/media/save", json=request.model_dump(by_alias=True)
        )

    # === Tags ===

    def create_tag(self, name: str, color: str = "D1CFD7") -> dict[str, Any]:
        """
        Create a tag.

        Args:
            name: Tag name
            color: Tag color (hex without #)

        Returns:
            Response data
        """
        request = CreateTagRequest(name=name, color=color)
        return self._post("/content/v2/tag", json=request.model_dump(by_alias=True))

    def delete_tag(self, tag_id: int) -> None:
        """
        Delete a tag.

        Args:
            tag_id: Tag ID
        """
        self._delete(f"/content/v2/tag/{tag_id}")
