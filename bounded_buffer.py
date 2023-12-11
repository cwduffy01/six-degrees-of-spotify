import collections

class BoundedBuffer(collections.UserList):
    size = 0

    def __init__(self, size: int, *args, **kwargs):
        self.size = size
        super(BoundedBuffer, self).__init__(*args, **kwargs)

    def push(self, item: None) -> None:
        if len(self.data) < self.size:
            return self.append(item)
        print("push not allowed, max size reached!")
    
    def pop(self, i: int = -1) -> None:
        return self.pop(i)
    
if __name__ == "__main__":
    bb = BoundedBuffer(3)
    bb.push(3)
    bb.push(3)
    bb.push(3)
    bb.push(3)
    print(bb)