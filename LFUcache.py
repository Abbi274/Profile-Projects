class Node: 
    def __init__(self, key = -1, val = -1, freq =1): 
        self.key = key 
        self.val = val
        self.freq = freq 
        self.next = None 
        self.prev = None 

class LRUCache: 
    def __init__(self, cache_key = 1):
        self.cache_key = cache_key 
        self.head = Node() 
        self.tail = Node() 
        self.head.next = self.tail 
        self.tail.prev = self.head 

    def add(self, node):
        node.prev = self.head
        node.next = self.head.next 
        self.head.next.prev = node
        self.head.next = node  
    
    def remove(self, node): 
        node.next.prev = node.prev 
        node.prev.next = node.next 
        return self.isempty()
            
    def remove_last(self):          
        lru = self.tail.prev
        if lru.prev == None: 
            print(lru.key, lru.val) 
        if lru == self.head: 
            raise Exception('Attempting to remove from empty cache')
        self.tail.prev = lru.prev 
        lru.prev.next = self.tail 
        return lru 

    def isempty(self): 
        return self.head.next == self.tail 

class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity 
        self.size = 0 
        self.lru_map = {} 
        self.key_node_map = {} 
        self.min_freq = 0 

    def get(self, key: int) -> int:
        if key not in self.key_node_map: 
            return -1 
        # update the freq 
        node = self.key_node_map[key] 
        node.freq += 1
        # remove from cur cache 
        lru_cache = self.lru_map[node.freq -1] 
        isempty = lru_cache.remove(node) 
        if isempty: 
            # if the cache is empty, update the min freq if needed and delete the cache 
            del self.lru_map[node.freq-1]
            if self.min_freq == node.freq -1: 
                self.min_freq += 1

        # add to new cache 
        if node.freq not in self.lru_map: 
            self.lru_map[node.freq] = LRUCache(node.freq)
        cur_cache = self.lru_map[node.freq]
        cur_cache.add(node) 
        
        return node.val
    def lru_map_add(self, node, node_freq): 
        if node_freq not in self.lru_map: 
            self.lru_map[node_freq] = LRUCache(node_freq)
        lru_cache = self.lru_map[node_freq] 
        lru_cache.add(node) 

    def put(self, key: int, value: int) -> None:

        if key not in self.key_node_map:

            if self.size == self.capacity:
                self.size -= 1
                lru_cache = self.lru_map[self.min_freq] 
                print(self.size, self.capacity, key, value)
                node = lru_cache.remove_last() 
                # remove reference to node 
                del self.key_node_map[node.key]

            new_node = Node(key, value)
            self.key_node_map[key] = new_node
            self.size += 1
            self.min_freq = 1 # either reaffirming as 1 or setting as 1 now that have a lru with freq = 1
            self.lru_map_add(new_node, new_node.freq)
        else: 
            self.key_node_map[key].val = value # update value 
            node = self.key_node_map[key] 
            # remove the node from cur cache  
            lru_cache = self.lru_map[node.freq] 
            isempty = lru_cache.remove(node) 
            if isempty: 
            # if the cache is empty, update the min freq if needed and delete the cache 
                del self.lru_map[node.freq]
                if self.min_freq == node.freq: 
                    self.min_freq += 1
            # add to new cache and update freq 
            node.freq += 1
            if node.freq not in self.lru_map: 
                self.lru_map[node.freq] = LRUCache(node.freq) 
            cur_cache = self.lru_map[node.freq]
            cur_cache.add(node)

        
        
params = [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
lfu = LFUCache(3)
for param in params: 
    if len(param) == 2: 
        lfu.put(param[0],param[1]) 
    else: 
        lfu.get(param[0]) 
print(lfu.key_node_map.keys())