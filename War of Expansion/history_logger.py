import json
import xml.etree.ElementTree as ET
import datetime
from xml.dom import minidom

def save_game_history(level_number, game_mode, ip_address, cells, connections, build_spots, turn_number=0, save_to_json=False, save_to_xml=False):
    try:
        game_data = {
            "level": level_number,
            "turn": turn_number,
            "mode": game_mode,
            "ip_address": ip_address if ip_address else "N/A",
            "start_time": datetime.datetime.now().isoformat(),
            "objects": {
                "cells": [
                    {
                        "type": cell.__class__.__name__,
                        "color": cell.color.name(),
                        "x": int(cell.pos().x()),
                        "y": int(cell.pos().y()),
                        "army": cell.army
                    } for cell in cells
                ],
                "connections": [
                    {
                        "from_x": int(conn[0].pos().x()),
                        "from_y": int(conn[0].pos().y()),
                        "to_x": int(conn[1].pos().x()),
                        "to_y": int(conn[1].pos().y())
                    } for conn in connections
                ],
                "build_spots": [
                    {
                        "x": int(spot.pos().x()),
                        "y": int(spot.pos().y()),
                        "owner": getattr(spot, "owner", "player")
                    } for spot in build_spots
                ]
            }
        }

        if save_to_json:
            print("Saving game data to JSON...")
            with open("last_game_history.json", "w", encoding="utf-8") as json_file:
                json.dump(game_data, json_file, ensure_ascii=False, indent=4)
            print("Game history saved to JSON.")
        
        if save_to_xml:
            print("Saving game data to XML...")
            root = ET.Element("GameHistory")
            ET.SubElement(root, "Level").text = str(level_number)
            ET.SubElement(root, "Turn").text = str(turn_number)
            ET.SubElement(root, "Mode").text = game_mode
            ET.SubElement(root, "IPAddress").text = ip_address if ip_address else "N/A"
            ET.SubElement(root, "StartTime").text = datetime.datetime.now().isoformat()

            objects = ET.SubElement(root, "Objects")

            # Cells
            cells_node = ET.SubElement(objects, "Cells")
            for cell in cells:
                cell_el = ET.SubElement(cells_node, "Cell")
                ET.SubElement(cell_el, "Type").text = cell.__class__.__name__
                ET.SubElement(cell_el, "Color").text = cell.color.name()
                ET.SubElement(cell_el, "X").text = str(int(cell.pos().x()))
                ET.SubElement(cell_el, "Y").text = str(int(cell.pos().y()))
                ET.SubElement(cell_el, "Army").text = str(cell.army)

            # Connections
            conns_node = ET.SubElement(objects, "Connections")
            for conn in connections:
                conn_el = ET.SubElement(conns_node, "Connection")
                ET.SubElement(conn_el, "FromX").text = str(int(conn[0].pos().x()))
                ET.SubElement(conn_el, "FromY").text = str(int(conn[0].pos().y()))
                ET.SubElement(conn_el, "ToX").text = str(int(conn[1].pos().x()))
                ET.SubElement(conn_el, "ToY").text = str(int(conn[1].pos().y()))

            # BuildSpots
            spots_node = ET.SubElement(objects, "BuildSpots")
            for spot in build_spots:
                spot_el = ET.SubElement(spots_node, "BuildSpot")
                ET.SubElement(spot_el, "X").text = str(int(spot.pos().x()))
                ET.SubElement(spot_el, "Y").text = str(int(spot.pos().y()))
                ET.SubElement(spot_el, "Owner").text = getattr(spot, "owner", "player")

            xml_str = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent="  ")
            with open("last_game_history.xml", "w", encoding="utf-8") as f:
                f.write(xml_str)
            print("Game history saved to XML.")

    except Exception as e:
        print(f"Error while saving game history: {e}")
