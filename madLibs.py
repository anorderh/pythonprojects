# global variables
inputReq = []
req = 'adj1 noun1 verbP1 adv adj2 noun2 noun3 adj3 verb1 adv2 verbP2 adj4'
preset = ['happy', 'penguin', 'fought', 'hastily', 'smelly', 'trumpet', 'flute',
          'tasty', 'run', 'sadly', 'galloped', 'confident']

# prompt for using preset
print('REQUIRED WORD COUNT: {0}\n'.format(len(preset)))
if 'y' == raw_input('Use a preset? "y" for YES, any other key for no\n').lower():
    print('using preset...\n')
    inputReq = preset
else:
    print('manuel input...\n')
    # for-each loop for input
    for word in req.split(' '):
        inputReq.append(raw_input('Insert! {0}\n'.format(word)))

# print story
print('MADLIB! "A Day at the Zoo!"\n\nToday I went to the zoo.\nI saw a(n) {0} {1} jumping up and down in its tree.\n'
      'He {2} {3} through the large tunnel that led to its {4} {5}.\nI got some peanuts and'
      ' passed them through the cage to a gigantic gray {6} towering above my head.\n'
      'Feeding that animal made me hungry.\nI went to get a {7} scoop of ice cream.\n'
      'It filled my stomach.\nAfterwards I had to {8} {9} to catch our bus.\n'
      'When I got home, I {10} my mom for a {11} day at the zoo.\n'
      .format(inputReq[0],inputReq[1],inputReq[2],inputReq[3],inputReq[4],inputReq[5],
              inputReq[6],inputReq[7],inputReq[8],inputReq[9],inputReq[10],inputReq[11])
      )


