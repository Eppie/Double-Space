import re
import csv
from math import log

csv_file = open("decisions.csv", "a+")
csvreader = csv.reader(csv_file)
csvwriter = csv.writer(csv_file)
csv_contents = []
headers = csvreader.next()
for row in csvreader:
  csv_contents.append(row)

# load the dicts from their files
try:
  d1 = eval(open('1.txt', 'r').read())
  d2 = eval(open('2.txt', 'r').read())
  d3 = eval(open('3.txt', 'r').read())
  d4 = eval(open('4.txt', 'r').read())
  d5 = eval(open('5.txt', 'r').read())
  d6 = eval(open('6.txt', 'r').read())
  d7 = eval(open('7.txt', 'r').read())
  d8 = eval(open('8.txt', 'r').read())
  d9 = eval(open('9.txt', 'r').read())
  d10 = eval(open('10.txt', 'r').read())
except:
  # only do this if the dict files do not exist
  d1 = dict()
  d2 = dict()
  d3 = dict()
  d4 = dict()
  d5 = dict()
  d6 = dict()
  d7 = dict()
  d8 = dict()
  d9 = dict()
  d10 = dict()

correct = [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0]
dicts = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]

testString = open("sample_text.txt", "r").read()
m = re.findall("(.{5})([\.?!] )(.{5})", testString)


# save the dicts
def writeResults():
  for i in range(10):
    f = open(str(i+1) + ".txt", "w+")
    f.write(str(dicts[i]))
    f.close()

  f = open("correct.txt", "w+")
  f.write(str(correct))
  f.close()


def freq(c,examples):
    count=0.0
    for e in examples:
        if e == c:
            count+=1
    return count


def info(examples):
    size = len(examples)
    result = 0
    for c in examples:
      try:
        temp=(freq(c,examples)/size)
        result+=temp*log(temp,2)
      except ValueError:
        pass
    return -1*result


def probabilistic_decision(arr, thresh=0.0):
  temp_sum = 0.0
  for i in range(10):
    key = arr[i]
    try:
      s = sum(dicts[i][key])/float(len(dicts[i][key]))
      if s < 0.5:
        s -= 1
      if s == 0:
        s = -1
      temp_sum += (100 - info(dicts[i][key])) * s
    except KeyError:
      pass
  prob = (temp_sum / 10.0) - 9.0
  if prob >= thresh:
    return 1, prob
  else:
    return 0, prob


def user_decision():
  s = raw_input("Replace? ")
  if s == "y":
    return 1
  elif s == "n":
    return 0
  elif s == "q":
    writeResults()
    quit()
  else:
    return user_decision()

right = 0
wrong = 0
for tuple in m:
  print tuple[0] + tuple[1] + tuple[2]
  ten_char = tuple[0] + tuple[2]
  dec = probabilistic_decision(ten_char)
  print dec
  replace = user_decision()
  correct.append(replace)

  if dec[0] == replace:
    right += 1
  else:
    wrong += 1

  print "Right: " + str(right) + ". Wrong: " + str(wrong) + "."
  csv_data = list(ten_char)
  csv_data.append(replace)
  csvwriter.writerow(csv_data)
  for i in range(10):
    if ten_char[i] in dicts[i]:
      dicts[i][ten_char[i]].append(replace)
    else:
      dicts[i][ten_char[i]] = [replace]

writeResults()
