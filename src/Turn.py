
class Turn:
    def __init__(self, rank, count, suits) -> None:
        self.rank = rank
        self.count = count
        self.suits = suits


    def __str__(self) -> str:
        return f"Rank: {self.rank}; Count: {self.count}; Suits: {self.suits}."
    

    # def __eq__(self, x) -> bool:
    #     if self.target
