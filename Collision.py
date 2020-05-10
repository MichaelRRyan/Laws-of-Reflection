def is_colliding(object1, object2):
    if object1.x + object1.width > object2.x and object1.x < object2.x + object2.width:
        if object1.y + object1.height > object2.y and object1.y < object2.y + object2.height:
            return True
    return False

def is_colliding_at(object1, object2, x, y):
    if x + object1.width > object2.x and x < object2.x + object2.width:
        if y + object1.height > object2.y and y < object2.y + object2.height:
            return True
    return False