from src.api.v1.params import Params


class ESSearcher:
    base = {"bool": {}}

    def __init__(
        self, params: Params, genre: str | None = None, title_query: str | None = None
    ) -> None:
        self.page_number = params.page_number
        self.page_size = params.page_size
        self._sort = params.sort.value
        self.genre = genre
        self.title_query = title_query

    def _build_match(self) -> dict:
        if self.title_query:
            return {"match": {"title": self.title_query}}
        return None

    def _build_filter(self) -> dict:
        if self.genre:
            return {"term": {"genre": self.genre}}
        return None

    def _build_sort(self) -> dict:
        t, field = self._sort[0], self._sort[1:]
        if t == '+':
            t = 'asc'
        elif t == '-':
            t = 'desc'

        return [{field: {'order': t}}]

    @property
    def query(self) -> dict:
        match = self._build_match()
        filter = self._build_filter()

        if match:
            self.base['bool']['must'] = {'match': match}
        if filter:
            self.base['bool']['filter'] = {'term': filter}

        return self.base

    @property
    def sort(self) -> list[dict]:
        if self.genre or not any([self.genre, self.title_query]):
            return self._build_sort()
        return None

    @property
    def from_(self) -> int:
        return (self.page_number - 1) * self.page_size

# GET /movies/_search
# {
#   "size": 10,
#   "from": 1,
#   "_source": ["id", "title", "imdb_rating"],
#   "query": {
#     "bool": {
#       "must": [
#         {"match": {"title": "star holiday"}}
#       ],
#       "filter": [
#         {"term": {
#           "genre": "Comedy"}}
#       ]
#     }
#   }
