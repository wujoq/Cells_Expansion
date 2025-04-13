import json
import xml.etree.ElementTree as ET
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor
from Cell import AttackCell, GeneratorCell, SupportCell, Cell
from BuildSpot import BuildSpot

def load_game_state(path):
    ext = path.split('.')[-1].lower()
    if ext == 'json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif ext == 'xml':
        data = _load_xml(path)
    else:
        raise ValueError("Unsupported file type")

    level = data["level"]
    turn = data.get("turn", 0)
    cells = _rebuild_cells(data["objects"]["cells"])
    connections = _rebuild_connections(data["objects"]["connections"], cells)
    build_spots = _rebuild_spots(data["objects"]["build_spots"], cells)

    return level, turn, cells, connections, build_spots

def _load_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    level = int(root.find("Level").text)
    turn = int(root.find("Turn").text) if root.find("Turn") is not None else 0

    cells = []
    for el in root.findall(".//Cell"):
        cells.append({
            "type": el.find("Type").text,
            "color": el.find("Color").text,
            "x": int(el.find("X").text),
            "y": int(el.find("Y").text),
            "army": int(el.find("Army").text)
        })

    connections = []
    for el in root.findall(".//Connection"):
        connections.append({
            "from_x": int(el.find("FromX").text),
            "from_y": int(el.find("FromY").text),
            "to_x": int(el.find("ToX").text),
            "to_y": int(el.find("ToY").text)
        })

    spots = []
    for el in root.findall(".//BuildSpot"):
        spots.append({
            "x": int(el.find("X").text),
            "y": int(el.find("Y").text),
            "owner": el.find("Owner").text
        })

    return {"level": level, "turn": turn, "objects": {
        "cells": cells, "connections": connections, "build_spots": spots
    }}

def _rebuild_cells(cell_data):
    result = []
    for c in cell_data:
        pos = QPointF(c["x"], c["y"])
        color = QColor(c["color"])
        cell_type = c["type"]

        if cell_type == "AttackCell":
            resource = (":/towers/attacking_unit_enemy.png" if color == QColor("red")
                        else ":/towers/attacking_unit.png")
            obj = AttackCell(100, pos, color, resource_path=resource)

        elif cell_type == "GeneratorCell":
            resource = (":/towers/generating_unit_enemy.png" if color == QColor("red")
                        else ":/towers/generating_unit.png")
            obj = GeneratorCell(100, pos, color, resource_path=resource)

        elif cell_type == "SupportCell":
            resource = (":/towers/support_unit_enemy.png" if color == QColor("red")
                        else ":/towers/support_unit.png")
            obj = SupportCell(100, pos, color, resource_path=resource)

        else:
            obj = Cell(100, pos, color)

        obj.army = c["army"]
        result.append(obj)
    return result

def _rebuild_connections(conn_data, all_cells):
    pos_map = {(round(c.pos().x()), round(c.pos().y())): c for c in all_cells}
    result = []
    for conn in conn_data:
        a = pos_map.get((conn["from_x"], conn["from_y"]))
        b = pos_map.get((conn["to_x"], conn["to_y"]))
        if a and b:
            result.append((a, b))
    return result

def _rebuild_spots(spot_data, all_cells):
    result = []

    for s in spot_data:
        pos = QPointF(s["x"], s["y"])
        skip = False

        for c in all_cells:
            cell_pos = c.pos()
            if int(cell_pos.x()) == int(pos.x()) and int(cell_pos.y()) == int(pos.y()):
                print(f"[INFO] Pomijam BuildSpot na ({pos.x()}, {pos.y()}) — zajęte przez wieżę.")
                skip = True
                break

        if skip:
            continue

        spot = BuildSpot(pos, 100, None)
        if s["owner"] == "AI":
            spot.is_ai = True
        result.append(spot)

    return result
