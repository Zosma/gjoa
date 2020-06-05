

class Glacier:
    def __init__(self, chunks):
        self.key = chunks
        self.padding = 256 - len(self.key) - self.num_ones()
        # Create the 'ocean'
        for i in range(0, self.padding):
            self.key.append(0)

    # Method to get the number of ones present in a set of bit chunks
    def num_ones(self):
        total = 0
        for chunk in self.key:
            total += chunk
        return chunk

    # Method for all chunks to move in proportional sequence
    def advance(self):
        self.key = self.key[len(self.key) - 1:] + self.key[:len(self.key) - 1]

    # Method for the chunk clusters to break apart from one another.
    def calve(self, index=0):
        if self.key[index] == 0:
            return 0
        # If the next placement is a padding, swap it with the desired index.
        if index + 1 < 256 and self.key[index+1] == 0:
            temp = self.key[index]
            self.key[index] = self.key[index+1]
            self.key[index + 1] = temp

    # Method for specific chunks to drift apart
    def drift(self):
        for chunk in self.key:
            print("derp")
        return 0

    # Method to mix(swap) the glacier positions (if they are different)
    def cycle(self):
        for chunk in self.key:
            print("derp")
        return 0

    def check_key(self):
        print("shit")