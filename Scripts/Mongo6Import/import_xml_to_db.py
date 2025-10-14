import sys
from config import get_connection
from xml_parser import parse_xml

def import_file(xml_path):
    print(f"⏳ Parsowanie XML: {xml_path}")
    systems = parse_xml(xml_path)

    db = get_connection()
    collection = db["star_systems"]

    inserted = 0
    try:
        for system in systems:
            doc = {
                "Name": system["Name"],
                "Location": system["Location"],
                "Stars": []
            }

            for star in system["Stars"]:
                star_doc = {
                    "Name": star["Name"],
                    "StarType": star.get("StarType"),
                    "StarSubType": star.get("StarSubType"),
                    "SpectralClass": star.get("SpectralClass"),
                    "Mass": star.get("Mass"),
                    "Size": star.get("Size"),
                    "Temperature": star.get("Temperature"),
                    "Age": star.get("Age"),
                    "Luminosity": star.get("Luminosity"),
                    "Photometry": {
                        "ApperentMagnitude": star.get("ApperentMagnitude"),
                        "AbsoluteMagnitude": star.get("AbsoluteMagnitude"),
                        "PhotometryK": star.get("PhotometryK"),
                        "PhotometryH": star.get("PhotometryH"),
                        "PhotometryJ": star.get("PhotometryJ"),
                        "PhotometryI": star.get("PhotometryI"),
                        "PhotometryG": star.get("PhotometryG"),
                        "PhotometryB": star.get("PhotometryB"),
                        "PhotometryU": star.get("PhotometryU"),
                    },
                    "Planets": star["Planets"]
                }
                doc["Stars"].append(star_doc)

            collection.insert_one(doc)
            inserted += 1

        print(f"🎉 Zaimportowano {inserted} systemów gwiezdnych do MongoDB.")
    except Exception as e:
        print("❌ Błąd:", e)
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python import_xml_to_db.py <plik.xml>")
        sys.exit(1)
    import_file(sys.argv[1])
