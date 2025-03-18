#!/usr/bin/env python3
import rospy
from moveit_msgs.msg import PlanningScene, CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose

def create_box_object(name, size, pose):
    """Create a MoveIt! CollisionObject for a box."""
    collision_object = CollisionObject()
    collision_object.id = name
    collision_object.header.frame_id = "world"
    collision_object.header.stamp = rospy.Time.now()
    collision_object.operation = CollisionObject.ADD

    # Define the box
    box = SolidPrimitive()
    box.type = SolidPrimitive.BOX
    box.dimensions = size  # [x, y, z]

    # Define the pose
    object_pose = Pose()
    object_pose.position.x = pose[0]
    object_pose.position.y = pose[1]
    object_pose.position.z = pose[2]
    object_pose.orientation.w = 1.0  # Quaternion needs w=1 for no rotation

    collision_object.primitives.append(box)
    collision_object.primitive_poses.append(object_pose)

    return collision_object

def create_cylinder_object(name, radius, length, pose):
    """Create a MoveIt! CollisionObject for a cylinder."""
    collision_object = CollisionObject()
    collision_object.id = name
    collision_object.header.frame_id = "world"
    collision_object.header.stamp = rospy.Time.now()
    collision_object.operation = CollisionObject.ADD

    # Define the cylinder
    cylinder = SolidPrimitive()
    cylinder.type = SolidPrimitive.CYLINDER
    cylinder.dimensions = [length, radius]  # [height, radius]

    # Define the pose
    object_pose = Pose()
    object_pose.position.x = pose[0]
    object_pose.position.y = pose[1]
    object_pose.position.z = pose[2]
    object_pose.orientation.w = 1.0  # Quaternion needs w=1 for no rotation

    collision_object.primitives.append(cylinder)
    collision_object.primitive_poses.append(object_pose)

    return collision_object

def main():
    rospy.init_node('add_objects_to_moveit', anonymous=True)

    scene_pub = rospy.Publisher('/planning_scene', PlanningScene, queue_size=10)

    rospy.sleep(2)  # Give time for the publisher to connect

    # Create MoveIt! collision objects for the work table
    tabletop = create_box_object("tabletop", [1.2, 1.2, 0.05], [0, 0, 0.4])
    drop_zone = create_box_object("drop_zone", [0.5, 0.5, 0.01], [0.2, 0.2, 0.425])

    # Create table legs
    leg_1 = create_cylinder_object("leg_1", 0.05, 0.4, [-0.5, -0.5, 0.2])
    leg_2 = create_cylinder_object("leg_2", 0.05, 0.4, [0.5, -0.5, 0.2])
    leg_3 = create_cylinder_object("leg_3", 0.05, 0.4, [-0.5, 0.5, 0.2])
    leg_4 = create_cylinder_object("leg_4", 0.05, 0.4, [0.5, 0.5, 0.2])

    # Create the blue cube
    blue_cube = create_box_object("blue_cube", [0.06, 0.06, 0.06], [0, 0, 0.5])

    # Publish to the planning scene
    planning_scene = PlanningScene()
    planning_scene.is_diff = True
    planning_scene.world.collision_objects.extend([
        tabletop, drop_zone, leg_1, leg_2, leg_3, leg_4, blue_cube
    ])

    # Publish multiple times to ensure the scene updates
    for _ in range(5):
        scene_pub.publish(planning_scene)
        rospy.sleep(1)

    rospy.loginfo("✅ Added work table and blue cube to the planning scene!")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
