import os, json

# TODO: Question: Why do we need this file? It doesn't seem to be referenced elsewhere
# Can you also annotate a bit with comments?
def return_dict(json_file):
    jsonObj = None
    with open(json_file) as dataFile:
        data = dataFile.read()
        #obj = '''['''+data[data.find('{') : data.rfind('}')+1]+''']'''
        jsonObj = json.loads(data)
    dataFile.close()
    return jsonObj

output_file = os.path.join('..', 'dump', 'filtered.json')
# print("output file", output_file)
tweet_dict = return_dict(output_file)
flatten_tweet_dict = {}

for tweet_thread in tweet_dict:
    for tweet in tweet_thread:
        #print("tweet", tweet)
        if str(tweet["id"]) in flatten_tweet_dict:
            print("already present for", flatten_tweet_dict[tweet["id"]])
        else:
            flatten_tweet_dict[str(tweet["id"])] = tweet["tweet"]

print("length of flatten tweet dict is", len(flatten_tweet_dict))
print(flatten_tweet_dict.keys())

labels = os.path.join('..', 'data', 'labels.json')
labels = return_dict(labels)
tagged = []

for tweet_thread in labels:
    for tweet in tweet_thread:
        print("new tweet is", tweet)
        tmp = {}
        tmp["id"] = str(tweet["text"])
        tmp["text"] = flatten_tweet_dict[str(tweet["text"])]
        tmp["tag"] = tweet["decision"]
        tagged.append(tmp)

s = json.dumps(tagged)
open("tagged_data.json", "w").write(s)
