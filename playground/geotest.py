import math
import wpimath.geometry
import numpy

rot270 = wpimath.geometry.Rotation3d( 0.0, 0.0, -math.pi/2 ) # -90 degree rotation in the xy plane
rot180 = wpimath.geometry.Rotation3d( 0.0, 0.0, math.pi )    # 180 degree rotation in the xy plane

o0 = wpimath.geometry.Pose3d()
t0 = wpimath.geometry.Translation3d( 1.0, 1.0, 1.0 )
r0 = wpimath.geometry.Rotation3d( 0.0, 0.0, math.pi/2 )
p0 = wpimath.geometry.Pose3d( t0, r0 )
X0 = wpimath.geometry.Transform3d( t0, r0 )

#dummy camera offset: 30cm right, 10cm back, 60cm elevated, 0.1rad elevation
ct = wpimath.geometry.Translation3d( 0.3, -0.1, 0.6 )
cr = wpimath.geometry.Rotation3d( 0.0, -0.1, 0.0)
Bc = wpimath.geometry.Transform3d( ct, cr )

def main():
  global p0
  print( "...Transform Tests...")
  print( p0 )
  p1 = p0.transformBy(X0)
  print( p1 )
  p2 = p1.transformBy(X0)
  print( p2 )

  print( "...Relative Transforms...")
  print( o0 )
  print( p0 )
  p1 = o0.relativeTo(p0)
  p0 = p0.relativeTo(p0)
  print( p0 )
  print( p1 )

  print( "..." )
  fb = wpimath.geometry.Pose3d( wpimath.geometry.Translation3d( 8.0, 4.0, 0.0 ), wpimath.geometry.Rotation3d( 0.0, 0.0, 0.0) )
  fc = wpimath.geometry.Pose3d( wpimath.geometry.Translation3d( 8.3, 3.9, 0.6 ), wpimath.geometry.Rotation3d( 0.0, -0.1, 0.0) )
  Tc = wpimath.geometry.Transform3d( fb, fc )
  print( Tc )

  print( "...Quaternion tests...")
  q0 = wpimath.geometry.Quaternion( 1.0, 0.0, 0.0, 0.0 )
  r0 = wpimath.geometry.Rotation3d( q0 )
  print( f"1000: {r0}" )
  q0 = wpimath.geometry.Quaternion( 0.0, 1.0, 0.0, 0.0 )
  r0 = wpimath.geometry.Rotation3d( q0 )
  print( f"0100: {r0}" )
  q0 = wpimath.geometry.Quaternion( 0.0, 0.0, 1.0, 0.0 )
  r0 = wpimath.geometry.Rotation3d( q0 )
  print( f"0010: {r0}" )
  q0 = wpimath.geometry.Quaternion( 0.0, 0.0, 0.0, 1.0 )
  r0 = wpimath.geometry.Rotation3d( q0 )
  print( f"0001: {r0}" )
  r0 = wpimath.geometry.Rotation3d( 0.0, 0.0, 0.0 )
  q0 = r0.getQuaternion()
  print( f"r000: {q0}" )
  r0 = wpimath.geometry.Rotation3d( 0.0, 0.0, math.pi/2 )
  q0 = r0.getQuaternion()
  print( f"r00u: {q0}" )
  r0 = wpimath.geometry.Rotation3d( 0.0, 0.0, math.pi )
  q0 = r0.getQuaternion()
  print( f"r00p: {q0}" )
  r0 = wpimath.geometry.Rotation3d( 0.0, 0.0, -math.pi/2 )
  q0 = r0.getQuaternion()
  print( f"r00d: {q0}" )

  print( "...Coordinate system test...")
  c0 = wpimath.geometry.Pose3d()
  b0 = wpimath.geometry.CoordinateSystem.convert( c0, wpimath.geometry.CoordinateSystem.EDN(), wpimath.geometry.CoordinateSystem.NWU() )
  print( f"c0: {c0}" )
  print( f"b0: {b0}" )
  c0 = wpimath.geometry.CoordinateSystem.convert( b0, wpimath.geometry.CoordinateSystem.NWU(), wpimath.geometry.CoordinateSystem.EDN() )
  print( f"c0: {c0}" )
  b0 = wpimath.geometry.Pose3d()
  c0 = wpimath.geometry.CoordinateSystem.convert( b0, wpimath.geometry.CoordinateSystem.NWU(), wpimath.geometry.CoordinateSystem.EDN() )
  print( f"b0: {b0}" )
  print( f"c0: {c0}" )
  b0 = wpimath.geometry.CoordinateSystem.convert( c0, wpimath.geometry.CoordinateSystem.EDN(), wpimath.geometry.CoordinateSystem.NWU() )
  print( f"b0: {b0}" )

  print( "...Vector to Rotation...")
  r0 = wpimath.geometry.Rotation3d( numpy.array([[1.0],[0.0],[0.0]]), numpy.array([[1.0],[0.0],[0.0]]) )
  print( f"nul: {r0}" )
  r0 = wpimath.geometry.Rotation3d( numpy.array([[1.0],[0.0],[0.0]]), numpy.array([[0.0],[0.0],[1.0]]) )
  print( f"rot: {r0}" )

  print("...Coordinate System...")
  print( X0 )
  XC = wpimath.geometry.CoordinateSystem.convert(X0,wpimath.geometry.CoordinateSystem.NWU(),wpimath.geometry.CoordinateSystem.EDN())
  print( f"XC: {XC}" )
  XB = wpimath.geometry.CoordinateSystem.convert(X0,wpimath.geometry.CoordinateSystem.EDN(),wpimath.geometry.CoordinateSystem.NWU())
  print( f"XB: {XB}" )

if __name__ == '__main__':
    main()
