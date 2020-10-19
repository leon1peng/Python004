import threading
import time


def wants_to_eat(philosopher, name):
    pick_left = philosopher.left.acquire()
    if pick_left:
        print(f"{name} 获取左叉子")
    pick_right = philosopher.right.acquire()
    if pick_right:
        print(f"{name} 获取右叉子")
        print(f"哲学家 {name} 开始就餐")
        time.sleep(2)
    philosopher.right.release()
    philosopher.left.release()


class DiningPhilosophers(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


if __name__ == '__main__':
    r_lock1 = threading.RLock()
    r_lock2 = threading.RLock()
    r_lock3 = threading.RLock()
    r_lock4 = threading.RLock()
    r_lock5 = threading.RLock()
    
    philosopher1 = DiningPhilosophers(r_lock5, r_lock1)
    philosopher2 = DiningPhilosophers(r_lock1, r_lock2)
    philosopher3 = DiningPhilosophers(r_lock2, r_lock3)
    philosopher4 = DiningPhilosophers(r_lock3, r_lock4)
    philosopher5 = DiningPhilosophers(r_lock4, r_lock5)

    run1 = threading.Thread(target=wants_to_eat, args=(philosopher1, "philosopher1"))
    run2 = threading.Thread(target=wants_to_eat, args=(philosopher2, "philosopher2"))
    run3 = threading.Thread(target=wants_to_eat, args=(philosopher3, "philosopher3"))
    run4 = threading.Thread(target=wants_to_eat, args=(philosopher4, "philosopher4"))
    run5 = threading.Thread(target=wants_to_eat, args=(philosopher5, "philosopher5"))

    run1.start()
    run2.start()
    run3.start()
    run4.start()
    run5.start()

