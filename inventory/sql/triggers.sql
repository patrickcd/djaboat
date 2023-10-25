DROP TABLE IF EXISTS search_index;

CREATE VIRTUAL TABLE search_index using fts5(
  object_text,
  object_id,
  content_table
);

/* ITEMS */

INSERT INTO search_index 
    SELECT (name || ' ' || notes), id, 'inventory_item' FROM inventory_item;

DROP TRIGGER IF EXISTS after_item_insert;

CREATE TRIGGER after_item_insert AFTER INSERT ON inventory_item BEGIN
  INSERT INTO search_index values( new.name || ' ' || new.notes, new.id, 'inventory_item');
END;

DROP TRIGGER IF EXISTS after_item_update;

CREATE TRIGGER after_item_update AFTER UPDATE ON inventory_item BEGIN
  UPDATE search_index SET object_text = (new.name || ' ' || new.notes) 
    WHERE object_id = new.id AND content_table = 'inventory_item';
END;

DROP TRIGGER IF EXISTS after_item_delete;

CREATE TRIGGER after_item_delete AFTER DELETE ON inventory_item BEGIN
  DELETE FROM search_index 
    WHERE search_index.object_id = old.id AND content_table = 'inventory_item';
END;

/* MAINTENANCE */

INSERT INTO search_index 
    SELECT task, id, 'inventory_maintenance' FROM inventory_maintenance;

DROP TRIGGER IF EXISTS after_maintenance_insert;

CREATE TRIGGER after_maintenance_insert AFTER INSERT ON inventory_maintenance BEGIN
  INSERT INTO search_index values( new.task, new.id, 'inventory_maintenance');
END;

DROP TRIGGER IF EXISTS after_maintenance_update;

CREATE TRIGGER after_maintenance_update AFTER UPDATE ON inventory_maintenance BEGIN
  UPDATE search_index SET object_text = (new.task) 
    WHERE object_id = new.id AND content_table = 'inventory_maintenance';
END;

DROP TRIGGER IF EXISTS after_maintenance_delete;

CREATE TRIGGER after_maintenance_delete AFTER DELETE ON inventory_maintenance BEGIN
  DELETE FROM search_index 
    WHERE search_index.object_id = old.id AND content_table = 'inventory_maintenance';
END;

/* MAINTENANCE LOG*/

INSERT INTO search_index 
    SELECT notes, id, 'inventory_maintenancelog' FROM inventory_maintenancelog;

DROP TRIGGER IF EXISTS after_maintenancelog_insert;

CREATE TRIGGER after_maintenancelog_insert AFTER INSERT ON inventory_maintenancelog BEGIN
  INSERT INTO search_index values( new.notes, new.id, 'inventory_maintenancelog');
END;

DROP TRIGGER IF EXISTS after_maintenancelog_update;

CREATE TRIGGER after_maintenancelog_update AFTER UPDATE ON inventory_maintenancelog BEGIN
  UPDATE search_index SET object_text = (new.notes) 
    WHERE object_id = new.id AND content_table = 'inventory_maintenancelog';
END;

DROP TRIGGER IF EXISTS after_maintenancelog_delete;

CREATE TRIGGER after_maintenancelog_delete AFTER DELETE ON inventory_maintenancelog BEGIN
  DELETE FROM search_index 
    WHERE search_index.object_id = old.id AND content_table = 'inventory_maintenancelog';
END;
