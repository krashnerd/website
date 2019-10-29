import NeuralNetwork

input_layer_size = 27
hidden_layer_models = [
]
hidden_layer_models.extend([[x] for x in range(5, 8)])
hidden_layer_models.extend([x, 5] for x in range(5, 8))

def main():

	network = NeuralNetwork.NeuralNetwork()





if __name__ == '__main__':
	main()