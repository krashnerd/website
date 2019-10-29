import tkinter as tk
from tk_gui import game_gui
import agents.players as player_module

def get_players():

	player_options = [
			("Human"),
			("Greedy"),
		]

	options_dict = {str(i+1):option for i, option in enumerate(player_options)}
	options_print = "Options:\n" + "\n".join("{}: {}".format(i+1, val) for i,val in enumerate(player_options))

	while True:
		try:
			num_players = int(input("How many players? "))
			if num_players not in range(2,5):
				raise ValueError
		except ValueError:
			print("Enter a number from 2 to 4")
		else:
			break

	players = []
	for player in range(1, num_players + 1):
		valid_input = False
		while not valid_input:
			player_type = input("\nPlayer {} type?\n{}\n\n> ".format(player, options_print))

			# Assume the input is valid until it is shown not to be.
			valid_input = True

			if player_type.lower() in [x.lower() for x in player_options]:
				players.append(player_type)

			elif player_type in options_dict:
				players.append(options_dict[player_type])

			else:
				print("Invalid input")
				valid_input = False

	return players










def main():
	index = {"Human": "human", "Greedy": player_module.GreedyPlayer()}
	player_types = get_players()
	players = [index[player_type] for player_type in player_types]

	# intro_win = tk.Tk()

	win = tk.Tk()

	game_display = game_gui.Display(win, players)
	win.mainloop()


if __name__ == '__main__':
	main()