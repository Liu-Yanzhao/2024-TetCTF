class reverse():
    def __init__(self, array):
        self.array = array
        self.newarray = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]

        array1 = [ 96,101, 20,177,155,116,108, 69, 84,109,103,110,111, 95,116,103, 97, 72, 20, 59]
        array2 = [ 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36, 19, 55, 32, 36]
        self.global_arr = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        
        for i in range(len(array1)):
            self.global_arr[i] = array1[i] ^ array2[i]
    
    def array_unfill(self, index):
        return self.array[index] - 19 + (-64)

    def three(self, index): # gets the value of the array at index
        return self.array[index]

    def reverse_four(self, index, indexplus1, arrayval=None):
        if index==0:
            temp = self.array_unfill(indexplus1)
            temp = temp ^ 32
            temp = temp - arrayval
            self.newarray[indexplus1] = temp
            print(self.newarray)
            pass
        elif index==1:
            temp = self.array_unfill(indexplus1)
            temp = temp ^ 36
            temp = temp - arrayval
            self.newarray[indexplus1] = temp
            print(self.newarray)
            pass
        elif index==2:
            temp = self.array_unfill(indexplus1)
            temp = temp ^ 19
            temp = temp - arrayval
            self.newarray[indexplus1] = temp
            print(self.newarray)
        elif index==3:
            temp = self.array_unfill(indexplus1)
            temp = temp ^ 55
            temp = temp - arrayval
            self.newarray[indexplus1] = temp
            print(self.newarray)


    def check_reverse(self):
        for i in range(19, -1, -4):
            temp = self.global_arr[i] ^ self.three(i)
            self.reverse_four(i%4, i+1-4, temp)

        for i in range(0, 20, 4):
            temp = self.global_arr[i] + self.newarray[i]
            self.reverse_four(i%4, i+1, temp)

        for i in range(1, 20, 4):
                temp = self.three(i) - self.global_arr[i]
                self.reverse_four(i%4, i+1, temp)

        for i in range(2, 20, 4):
                temp = self.three(i) * self.global_arr[i]
                self.reverse_four(i%4, i+1, temp)

    def toascii(self):
        text = ""
        for i in self.newarray:
            text += chr(i - 19 + (-64))
        print(text)



reversed = reverse([38793, 584, 738, 38594, 63809, 647, 833, 63602, 47526, 494, 663, 47333, 67041, 641, 791, 66734, 35553, 561, 673, 35306])
reversed.check_reverse()
reversed.toascii()    