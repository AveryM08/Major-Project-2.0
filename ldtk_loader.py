import json
import os
import pygame
from typing import Dict, List, Tuple, Optional, Any

class LDtkProject:
    """
    Loads an LDtk .ldtk JSON project and exposes accessors for worlds, levels,
    layers, tilesets, and entities. Designed for grid-based tile layers and
    typical entity workflows.
    """

    def __init__(self, project_path: str, tileset_dir: str = "assets/tilesets"):
        self.project_path = project_path
        self.tileset_dir = tileset_dir
        self.data = self._load_json(project_path)
        self.defs = self.data.get("defs", {})
        self.levels = self.data.get("levels", [])
        self.tilesets = self._index_tilesets()
        self.layer_defs = self._index_layer_defs()
        self.entity_defs = self._index_entity_defs()
        self._tileset_surfaces = {}
        self._load_tileset_surfaces()

    # --------------------------
    # Core IO
    # --------------------------
    def _load_json(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # --------------------------
    # Indexing LDtk definitions
    # --------------------------
    def _index_tilesets(self) -> Dict[int, dict]:
        ts_defs = self.defs.get("tilesets", [])
        return {ts["uid"]: ts for ts in ts_defs}

    def _index_layer_defs(self) -> Dict[int, dict]:
        layer_defs = self.defs.get("layers", [])
        return {ld["uid"]: ld for ld in layer_defs}

    def _index_entity_defs(self) -> Dict[int, dict]:
        entity_defs = self.defs.get("entities", [])
        return {ed["uid"]: ed for ed in entity_defs}

    # --------------------------
    # Tileset assets (pygame surfaces)
    # --------------------------
    def _load_tileset_surfaces(self):
        for uid, ts in self.tilesets.items():
            rel = ts.get("relPath") or ts.get("path")
            if not rel:
                continue
            img_path = os.path.join(self.tileset_dir, os.path.basename(rel))
            if os.path.exists(img_path):
                self._tileset_surfaces[uid] = pygame.image.load(img_path).convert_alpha()

    def get_tileset_surface(self, tileset_uid: int) -> Optional[pygame.Surface]:
        return self._tileset_surfaces.get(tileset_uid)

    # --------------------------
    # Levels and layers access
    # --------------------------
    def list_level_identifiers(self) -> List[str]:
        return [lvl["identifier"] for lvl in self.levels]

    def get_level(self, identifier_or_index) -> dict:
        if isinstance(identifier_or_index, int):
            return self.levels[identifier_or_index]
        for lvl in self.levels:
            if lvl["identifier"] == identifier_or_index:
                return lvl
        raise KeyError(f"Level not found: {identifier_or_index}")

    def get_layer_instances(self, level: dict) -> List[dict]:
        return level.get("layerInstances", []) or []

    def get_layer_tileset_uid(self, layer: dict) -> Optional[int]:
        return layer.get("tilesetDefUid")

    def is_auto_layer(self, layer: dict) -> bool:
        return layer.get("__type") == "AutoLayer"

    def is_tiles_layer(self, layer: dict) -> bool:
        return layer.get("__type") == "Tiles"

    def is_entities_layer(self, layer: dict) -> bool:
        return layer.get("__type") == "Entities"

    # --------------------------
    # Tiles access
    # --------------------------
    def get_tiles(self, layer: dict) -> List[dict]:
        tiles = []
        tiles.extend(layer.get("gridTiles", []) or [])
        tiles.extend(layer.get("autoLayerTiles", []) or [])
        return tiles

    def get_tile_uv(self, tile: dict) -> Tuple[int, int, int, int]:
        r = tile.get("srcRect", {})
        return r.get("x", 0), r.get("y", 0), r.get("w", 0), r.get("h", 0)

    def get_tile_world_pos(self, tile: dict, layer: dict) -> Tuple[int, int]:
        px = tile.get("px", [0, 0])
        lx = layer.get("__pxTotalOffsetX", 0)
        ly = layer.get("__pxTotalOffsetY", 0)
        return px[0] + lx, px[1] + ly

    # --------------------------
    # Entities access
    # --------------------------
    def get_entities(self, layer: dict) -> List[dict]:
        return layer.get("entityInstances", []) or []

    def get_entity_identifier(self, ent: dict) -> str:
        return ent.get("__identifier", "")

    def get_entity_world_pos(self, ent: dict) -> Tuple[int, int]:
        return ent.get("__worldX", 0), ent.get("__worldY", 0)

    def get_entity_fields(self, ent: dict) -> Dict[str, Any]:
        fields = {}
        for f in ent.get("fieldInstances", []) or []:
            fields[f.get("__identifier")] = f.get("__value")
        return fields

    # --------------------------
    # Utility
    # --------------------------
    @staticmethod
    def world_to_screen(world_pos: Tuple[int, int], camera: Tuple[int, int]) -> Tuple[int, int]:
        return world_pos[0] - camera[0], world_pos[1] - camera[1]


class LDtkRenderer:
    """
    Renders LDtk levels and layers into a pygame Surface.
    """

    def __init__(self, project: LDtkProject, screen: pygame.Surface):
        self.project = project
        self.screen = screen

    def render_level(self, level: dict, camera: Tuple[int, int] = (0, 0)):
        for layer in reversed(self.project.get_layer_instances(level)):
            if self.project.is_tiles_layer(layer) or self.project.is_auto_layer(layer):
                self._render_tile_layer(layer, camera)
            elif self.project.is_entities_layer(layer):
                self._render_entities_layer(layer, camera)

    def _render_tile_layer(self, layer: dict, camera: Tuple[int, int]):
        tileset_uid = self.project.get_layer_tileset_uid(layer)
        if tileset_uid is None:
            tiles = self.project.get_tiles(layer)
            if tiles:
                tileset_uid = tiles[0].get("tilesetUid")
        if tileset_uid is None:
            return

        tileset_surf = self.project.get_tileset_surface(tileset_uid)
        if tileset_surf is None:
            return

        for tile in self.project.get_tiles(layer):
            uvx, uvy, uvw, uvh = self.project.get_tile_uv(tile)
            src = pygame.Rect(uvx, uvy, uvw, uvh)
            wx, wy = self.project.get_tile_world_pos(tile, layer)
            sx, sy = self.project.world_to_screen((wx, wy), camera)
            self.screen.blit(tileset_surf, (sx, sy), src)

    def _render_entities_layer(self, layer: dict, camera: Tuple[int, int]):
        for ent in self.project.get_entities(layer):
            ex, ey = self.project.get_entity_world_pos(ent)
            lx = layer.get("__pxTotalOffsetX", 0)
            ly = layer.get("__pxTotalOffsetY", 0)
            sx, sy = self.project.world_to_screen((ex + lx, ey + ly), camera)
            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(sx - 4, sy - 4, 8, 8))