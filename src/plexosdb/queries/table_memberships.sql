SELECT p.name AS parent_collection, po.name AS parent_object, co.name AS child_object
FROM t_membership m
LEFT JOIN t_object po ON m.parent_object_id = po.object_id
LEFT JOIN t_collection p ON m.parent_collection_id = p.collection_id
LEFT JOIN t_object co ON m.child_object_id = co.object_id
${where_clause}
