class ComparisionResult:
    def __init__(self, uniprotId, percentage, eValue, score=None):
        self.uniprotId=uniprotId
        self.percentage=percentage
        self.eValue=eValue
        self.score=None

class ResultFilterer:
    def __init__(self, blastResults, hhSearchResults):
        self.blastResults=blastResults
        self.hhSearchResults=hhSearchResults

    def filterTopResults(self):
        topResults = list()
        # some awesome logic goes here
        # work with Percentage of identity & work with eValue
        for result in self.blastResults:
            if result.percentage>90:
                if result.eValue<1:
                    topResults=topResults + result
  
        # combine them!
        return topResults