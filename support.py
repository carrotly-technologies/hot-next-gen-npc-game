from pygame.math import Vector2

def check_connections(radius, entity, target, tolerance = 30):

	relation = Vector2(target.rect.center) - Vector2(entity.rect.center)
	if relation.length() < radius:
		if entity.facing_direction == 'left' and relation.x < 0 and abs(relation.y) < tolerance or\
		   entity.facing_direction == 'right' and relation.x > 0 and abs(relation.y) < tolerance or\
		   entity.facing_direction == 'up' and relation.y < 0 and abs(relation.x) < tolerance or\
		   entity.facing_direction == 'down' and relation.y > 0 and abs(relation.x) < tolerance:
			return True