import asyncio
from .util import get, run


class AuthorStub:

    def __init__(self, **kwargs):
        self.authorId = kwargs["authorId"]
        self.name = kwargs.get("name", None)
        self.url = kwargs.get("url", None)

    def __str__(self):
        return self.authorId

    def __eq__(self, other):
        return isinstance(other, AuthorStub) and self.authorId == other.authorId

    def __hash__(self):
        return hash(self.authorId)

    def json(self):
        return {
            "authorId": self.authorId,
            "name": self.name,
            "url": self.url
        }

    async def full(self, **kwargs):
        return await SemanticScholarAPI.author(self.authorId, **kwargs)

    @property
    def complete(self):
        return SemanticScholarAPISync.author(self.authorId)


class Author:

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.authorId = kwargs["authorId"]
        self.name = kwargs.get("name", None)
        self.aliases = kwargs.get("aliases", [])
        self.citationVelocity = kwargs.get("citationVelocity", None)
        self.influentialCitationCount = kwargs.get("influentialCitationCount", None)
        self.url = kwargs.get("url", None)

    def __str__(self):
        return self.authorId

    def __eq__(self, other):
        return isinstance(other, Author) and self.authorId == other.authorId

    def __hash__(self):
        return hash(self.authorId)

    def papers(self):
        for elem in self._kwargs.get("papers", []):
            yield SemanticScholarAPI.paper(elem["paperId"])

    def json(self):
        return self._kwargs


class PaperStub:

    def __init__(self, **kwargs):
        self.paperId = kwargs["paperId"]
        self.isInfluential = kwargs.get("isInfluential", False)
        self.title = kwargs.get("title", None)
        self.venue = kwargs.get("venue", None)
        self.year = kwargs.get("year", None)

    def __str__(self):
        return self.paperId

    def __eq__(self, other):
        return isinstance(other, PaperStub) and self.paperId == other.paperId

    def __hash__(self):
        return hash(self.paperId)

    def json(self):
        return {
            "paperId": self.paperId,
            "isInfluential": self.isInfluential,
            "title": self.title,
            "venue": self.venue,
            "year": self.year,
        }

    async def full(self, **kwargs):
        return await SemanticScholarAPI.paper(self.paperId, **kwargs)

    @property
    def complete(self):
        return SemanticScholarAPISync.paper(self.paperId)


class Paper:

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.doi = kwargs.get("doi", None)
        self.citationVelocity = kwargs.get("citationVelocity", None)
        self.influentialCitationCount = kwargs.get("influentialCitationCount", None)
        self.url = kwargs.get("url", None)
        self.authors = [AuthorStub(**elem) for elem in kwargs.get("authors", [])]
        self.citations = [PaperStub(**elem) for elem in kwargs.get("citations", [])]
        self.references = [PaperStub(**elem) for elem in kwargs.get("references", [])]
        self.venue = kwargs.get("venue", None)
        self.references = kwargs.get("references", [])
        self.title = kwargs.get("title", None)
        self.year = kwargs.get("year", None)
        self.paperId = kwargs.get("paperId", None)

    def __str__(self):
        return self.paperId

    def __eq__(self, other):
        return isinstance(other, Paper) and self.paperId == other.paperId

    def __hash__(self):
        return hash(self.paperId)

    def json(self):
        return self._kwargs


class SemanticScholarAPI:
    BASE_URL = "http://api.semanticscholar.org/v1"
    AUTHOR_ENDPOINT = "{}/{}".format(BASE_URL, "author")
    PAPER_ENDPOINT = "{}/{}".format(BASE_URL, "paper")

    @staticmethod
    async def paper(paper_id, **kwargs):
        url = "{}/{}".format(SemanticScholarAPI.PAPER_ENDPOINT, paper_id)
        json = await get(url, params=kwargs)

        if json:
            return Paper(**json)

    @staticmethod
    async def author(author_id, **kwargs):
        url = "{}/{}".format(SemanticScholarAPI.AUTHOR_ENDPOINT, author_id)
        json = await get(url, params=kwargs)

        if json:
            return Author(**json)


    @staticmethod
    def pdf_url(paper_id):
        return "http://pdfs.semanticscholar.org/{}/{}.pdf".format(paper_id[:4], paper_id[4:])


class SemanticScholarAPISync(SemanticScholarAPI):
    @staticmethod
    def paper(paper_id, **kwargs):
        return run(SemanticScholarAPI.paper(paper_id, **kwargs))

    @staticmethod
    def author(author_id, **kwargs):
        return run(SemanticScholarAPI.author(author_id, **kwargs))
