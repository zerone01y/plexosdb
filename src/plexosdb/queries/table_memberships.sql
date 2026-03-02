SELECT parent_class.name AS parent_class, child_class.name AS child_class, coll.name AS collection, parent_obj.name AS parent_object, child_obj.name AS child_object
FROM t_membership m
LEFT JOIN t_object parent_obj ON m.parent_object_id = parent_obj.object_id
LEFT JOIN t_object child_obj ON m.child_object_id = child_obj.object_id
LEFT JOIN t_class parent_class ON m.parent_class_id = parent_class.class_id
LEFT JOIN t_class child_class ON m.child_class_id = child_class.class_id
LEFT JOIN t_collection coll ON m.collection_id = coll.collection_id
${where_clause}
