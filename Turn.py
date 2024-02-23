
class Turn:
    def __init__(self, target, rank, count, suits) -> None:
        self.target = target
        self.rank = rank
        self.count = count
        self.suits = suits


    def __str__(self) -> str:
        return f"Rank: {self.rank}; Count: {self.count}; Suits: {self.suits}."
