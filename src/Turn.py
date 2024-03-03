
class Turn:
    def __init__(self, target_id, rank, count, suits) -> None:
        self.target_id = target_id
        self.rank = rank
        self.count = count
        self.suits = suits


    def __str__(self) -> str:
        return f"Target: {self.target_id}; Rank: {self.rank}; Count: {self.count}; Suits: {self.suits}."
    

    # def __eq__(self, x) -> bool:
    #     if self.target
