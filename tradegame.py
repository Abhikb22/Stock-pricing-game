import random
import time

class TradingGame:
    def __init__(self, initial_balance=1000):
        self.players = {
            "Player 1": {"balance": initial_balance, "portfolio": {}},
            "Player 2": {"balance": initial_balance, "portfolio": {}},
        }
        self.stock_price = 100  # Initial stock price
        self.rounds = 10  # Total rounds in the game
        self.current_player = "Player 1"  # Start with Player 1

    def update_stock_price(self):
        """Randomly update the stock price."""
        change = random.uniform(-10, 10)  # Price changes between -10 and +10
        self.stock_price += change
        self.stock_price = max(1, self.stock_price)  # Ensure price doesn't go below 1

    def buy_from_market(self, player, quantity):
        """Buy a specific quantity of the stock from the market."""
        cost = quantity * self.stock_price
        if cost > self.players[player]["balance"]:
            print(f"{player}, you don't have enough balance to buy!")
        else:
            self.players[player]["balance"] -= cost
            self.players[player]["portfolio"]["stock"] = self.players[player]["portfolio"].get("stock", 0) + quantity
            print(f"{player} bought {quantity} shares from the market at ${self.stock_price:.2f} each.")

    def sell_to_market(self, player, quantity):
        """Sell a specific quantity of the stock to the market."""
        if self.players[player]["portfolio"].get("stock", 0) < quantity:
            print(f"{player}, you don't have enough shares to sell!")
        else:
            self.players[player]["balance"] += quantity * self.stock_price
            self.players[player]["portfolio"]["stock"] -= quantity
            print(f"{player} sold {quantity} shares to the market at ${self.stock_price:.2f} each.")

    def trade_between_players(self, seller, buyer, quantity, price):
        """Trade stocks between Player 1 and Player 2."""
        if self.players[seller]["portfolio"].get("stock", 0) < quantity:
            print(f"{seller}, you don't have enough shares to sell!")
        elif self.players[buyer]["balance"] < quantity * price:
            print(f"{buyer}, you don't have enough balance to buy!")
        else:
            # Seller sells shares
            self.players[seller]["portfolio"]["stock"] -= quantity
            self.players[seller]["balance"] += quantity * price
            # Buyer buys shares
            self.players[buyer]["portfolio"]["stock"] = self.players[buyer]["portfolio"].get("stock", 0) + quantity
            self.players[buyer]["balance"] -= quantity * price
            print(f"{seller} sold {quantity} shares to {buyer} at ${price:.2f} each.")

    def show_portfolio(self, player):
        """Display a player's balance and portfolio."""
        print(f"\n{player}'s Portfolio:")
        print(f"Balance: ${self.players[player]['balance']:.2f}")
        print(f"Shares owned: {self.players[player]['portfolio'].get('stock', 0)}")
        print(f"Current stock price: ${self.stock_price:.2f}")

    def switch_player(self):
        """Switch turns between Player 1 and Player 2."""
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

    def play_round(self, round_number):
        """Play one round of the game."""
        print(f"\n--- Round {round_number} ---")
        self.update_stock_price()
        self.show_portfolio("Player 1")
        self.show_portfolio("Player 2")

        print(f"\nIt's {self.current_player}'s turn!")
        action = input(f"{self.current_player}, what do you want to do? (buy/sell/trade/nothing): ").strip().lower()
        if action == "buy":
            quantity = int(input("How many shares do you want to buy from the market? "))
            self.buy_from_market(self.current_player, quantity)
        elif action == "sell":
            quantity = int(input("How many shares do you want to sell to the market? "))
            self.sell_to_market(self.current_player, quantity)
        elif action == "trade":
            other_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
            quantity = int(input(f"How many shares do you want to trade with {other_player}? "))
            price = float(input(f"At what price per share? (Current market price: ${self.stock_price:.2f}): "))
            self.trade_between_players(self.current_player, other_player, quantity, price)
        elif action == "nothing":
            print(f"{self.current_player} chose to do nothing.")
        else:
            print("Invalid action. Skipping this turn.")

        self.switch_player()  # Switch to the other player for the next round

    def calculate_net_worth(self, player):
        """Calculate a player's net worth (balance + value of shares)."""
        shares = self.players[player]["portfolio"].get("stock", 0)
        return self.players[player]["balance"] + (shares * self.stock_price)

    def play_game(self):
        """Run the trading game."""
        print("Welcome to the Two-Player Trading Game!")
        print("Each player starts with $1000 and 10 rounds to make as much money as possible.")
        print("The stock price will change randomly each round. Players can trade with each other. Good luck!\n")

        for round_number in range(1, self.rounds + 1):
            self.play_round(round_number)

        print("\n--- Game Over ---")
        player1_net_worth = self.calculate_net_worth("Player 1")
        player2_net_worth = self.calculate_net_worth("Player 2")
        print(f"Player 1's net worth: ${player1_net_worth:.2f}")
        print(f"Player 2's net worth: ${player2_net_worth:.2f}")

        if player1_net_worth > player2_net_worth:
            print("Player 1 wins!")
        elif player2_net_worth > player1_net_worth:
            print("Player 2 wins!")
        else:
            print("It's a tie!")

# Run the game
if __name__ == "__main__":
    game = TradingGame()
    game.play_game()