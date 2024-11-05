import json


class DataProcess:
    @staticmethod
    def get_json_content(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {}

    @staticmethod
    def set_json_content(json_path, json_data):
        try:
            data = DataProcess.get_json_content(json_path)
            search_list = [item for item in data if item["id"] == json_data["id"]]
            if len(search_list) != 0:
                for item in data:
                    if item["id"] == json_data["id"]:
                        item.update(json_data)
            else:
                data.append(json_data)

            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
        except Exception as e:
            print(f"Error in processing JSON file: {e}")

    @staticmethod
    def delete_json_content(json_path, id):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            data.remove([item for item in data if item["id"] == id][0])
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {}

    @staticmethod
    def write_json_content(json_path, json_data):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            data.update(json_data)
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
        except Exception as e:
            print(f"Error in writing JSON file: {e}")
