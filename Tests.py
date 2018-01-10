import tensorflow as tf

# --- Mac Version ---
# insert the file you wanna load here
fileName = 'sQXC5MkzFbbDCB3H78YZu8.hsreplay.xml'
pars = Pars()
# load the file to game
# game = hsDoc.from_xml_file(fileName)
while input() != "quit":
    f = open("/Applications/Hearthstone/Logs/Power.log", "r")
    # f = open("C:\Program Files (x86)\Hearthstone\Logs\Power.log", "r")
    myList = []
    for line in f:
        myList.append(line)
    f.close()
# --- ---

x = tf.placeholder("float", [None, 3])
y = x * 2


with tf.Session() as session:
    x_data = [[1, 2, 3],
              [4, 5, 6],]
    result = session.run(y, feed_dict={x: x_data})
    print(result)