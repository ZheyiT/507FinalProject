import json

Squad_JSON = 'AF_squad.json'
DistinctPlane_JSON_NM = 'AF_squad_updated.json'

with open(Squad_JSON) as f:
    cache_contents = f.read()
    Squad_CD = json.loads(cache_contents)

    for i in Squad_CD:
        pt = i["aircraft_url"]

        if pt in ["/wiki/F-16_Fighting_Falcon", "/wiki/F-16_Falcon"]:
            i["BAid"] = "F16"
        elif pt in ["/wiki/F-15_Eagle", "/wiki/F-15E_Strike_Eagle"]:
            i["BAid"] = "F15"
        elif pt in ["/wiki/F-35", "/wiki/F-15E_Strike_Eagle"]:
            i["BAid"] = "F35"
        elif pt == "/wiki/F-22_Raptor":
            i["BAid"] = "F22"
        else:
            i["BAid"] = "NA"

    dumped_json_cache = json.dumps(Squad_CD)
    fw = open(DistinctPlane_JSON_NM, "w")
    fw.write(dumped_json_cache)
    fw.close()