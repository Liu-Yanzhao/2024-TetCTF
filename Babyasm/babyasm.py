import sys

class babyasm(): 
    def __init__(self, array):
        self.array = array
        self.array = [ord(i) for i in self.array]

        array1 = [ 96,101, 20,177,155,116,108, 69, 84,109,103,110,111, 95,116,103, 97, 72, 20, 59]
        array2 = [ 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36]
        self.global_arr = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        
        for i in range(len(array1)):
            self.global_arr[i] = array1[i] ^ array2[i]
        

    def array_fill(self, index, value): # array[index] = value+83
        self.array[index] = value + 19 - (-64)

    def three(self, index): # gets the value of the array at index
        return self.array[index]

    def four(self, index, indexplus1, arrayval):
        if index == 0:
            indexp1_val = self.three(indexplus1) 
            temp = arrayval + indexp1_val
            temp = temp ^ 32 #xored with 32
            self.array_fill(indexplus1, temp)
        elif index == 1:
            indexp1_val = self.three(indexplus1) 
            temp = arrayval + indexp1_val
            temp = temp ^ 36 #xored with 36
            self.array_fill(indexplus1, temp)
        elif index == 2:
            indexp1_val = self.three(indexplus1) 
            temp = arrayval + indexp1_val
            temp = temp ^ 19 #xored with 19
            self.array_fill(indexplus1, temp)
        elif index == 3:
            indexp1_val = self.three(indexplus1) 
            temp = arrayval + indexp1_val
            temp = temp ^ 55 #xored with 55
            self.array_fill(indexplus1, temp)

    def five(self):
        answer = [38793, 584, 738, 38594, 63809, 647, 833, 63602, 47526, 494, 663, 47333, 67041, 641, 791, 66734, 35553, 561, 673, 35306]
        var = 0
        for i in range(19):
            if self.array[i] == answer[i]:
                var = var + 1
            else:
                pass
                # sys.exit(0)
        
        if var == 20:
            return 1 # accepted
        else:
            return 0 # rejected
    
    def check(self):
        for i in range(20):
            # for num in self.array: print(num)
            # print("")
            remainder = i%4
            if remainder == 0:
                temp = self.global_arr[i] + self.three(i)
                self.four(i%4, i+1, temp)
            elif remainder == 1:
                temp = self.three(i) - self.global_arr[i]
                print(self.three(i), self.global_arr[i])
                self.four(i%4, i+1, temp)
            elif remainder == 2:
                temp = self.global_arr[i] * self.three(i)
                self.four(i%4, i+1, temp)
            elif remainder == 3:
                temp = self.global_arr[i] ^ self.three(i)
                self.four(i%4, i+1-4, temp)
        self.five()
	
test = babyasm(['A','B','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','A','}'])
# for num in test.global_arr: print(num)
for i in range(len(test.array)):
    test.array_fill(i, test.array[i])


test.check()

print(test.array)


# [37635, 526, 711, 37222, 46871, 483, 611, 46654, 42087, 418, 587, 41925, 53589, 471, 634, 53474, 31793, 525, 601, 31562]
