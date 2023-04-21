import 'package:flutter/material.dart';
import 'package:etoile_project/widgets/nav-drawer.dart';

class FirstFloor extends StatelessWidget {
  const FirstFloor({super.key});

  @override
  Widget build(BuildContext context) {
    Widget textSection = const Padding(
      padding: EdgeInsets.all(30),
      child: Text(
        'This is the plan of the first floor of the Etoile Building',
        softWrap: true,
      ),
    );

    return Scaffold(
      drawer: NavDrawer(),
      appBar: AppBar(
        title: const Text('Menu'),
      ),
      body: ListView(
        children: [
          Image.asset(
            'images/test_banniere.jpg',
            fit: BoxFit.cover,
          ),
          textSection,
          MonLogo(),
          Transform.rotate(
            angle: 90 * 3.14159 / 180, // rotation de 90 degrés en radians
            child: Image(
              image: AssetImage('images/floor1.jpg'),
              height: 1500,
            ),
          )
        ],
      ),
    );
  }
}

class MonLogo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: LogoPainter(),
      child: Container(
        height: 200.0,
        width: 200.0,
      ),
    );
  }
}

class LogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    var paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    // dessiner un cercle
    canvas.drawCircle(
        Offset(size.width / 2, size.height / 2), size.width / 3, paint);

    // dessiner une ligne
    paint.color = Colors.green;
    canvas.drawLine(Offset(size.width / 2, size.height / 2),
        Offset(size.width / 2, size.height * 0.75), paint);

    // dessiner une courbe quadratique
    paint.color = Colors.red;
    Path path = Path();
    path.moveTo(size.width / 2, size.height / 2);
    path.quadraticBezierTo(
        size.width * 0.75, size.height * 0.5, size.width / 2, size.height / 4);
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return false;
  }
}

class Plan extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: PlanPainter(),
      child: Container(
        height: 200.0,
        width: 200.0,
      ),
    );
  }
}

class PlanPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    var paint = Paint()
      ..color = Colors.black
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    var rect = Rect.fromPoints(Offset(50.0, 50.0), Offset(150.0, 150.0));
    canvas.drawRect(rect, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return false;
  }
}
