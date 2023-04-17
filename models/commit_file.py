from pydantic import BaseModel
from typing import List

class CommitFile(BaseModel):
    path: List[str] | None = None
    filename: str | None = None
    extension: str | None = None
    prefix: str = ""
    
    def toFilename(self):
        return f"{self.prefix}{self.filename}"
    def toString(self):
        return f"{self.toFilename()}.{self.extension}" if self.extension else self.toFilename()
    def pathToString(self):
        return "/".join(self.path)
    def toFullString(self):
        return f"{self.pathToString()}/{self.toString()}" if self.path else self.toString()

