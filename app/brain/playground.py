from utils import read_json_to_dict
import pprint
import json






report = read_json_to_dict("./_temp/report.json")
pprint.pprint(shake_similarity_report(report))