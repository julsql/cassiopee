import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:etoile_project/widgets/nav-drawer.dart';
import 'package:flutter/services.dart';

class SecondFloor extends StatefulWidget {
  const SecondFloor({super.key});

  @override
  State<SecondFloor> createState() => _SecondFloorState();
}

class _SecondFloorState extends State<SecondFloor> {
  List _items = [];

  // Fetch content from the json file
  Future<void> readJson() async {
    final String response = await rootBundle.loadString('json/sample.json');
    final data = await json.decode(response);
    setState(() {
      _items = data["items"];
    });
  }

  void _drawRectangle(Canvas canvas, Size size) {
    final List<List<double>> rectanglePoints = [
      [9.22, 0.2],
      [15.38, 0.2],
      [15.38, 3.07],
      [9.22, 3.07],
      [9.22, 0.2]
    ];

    final Paint paint = Paint()
      ..color = Colors.blue
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final path = Path();
    path.moveTo(rectanglePoints[0][0]*10, rectanglePoints[0][1]*10);

    for (int i = 1; i < rectanglePoints.length; i++) {
      final x = rectanglePoints[i][0]*10;
      final y = rectanglePoints[i][1]*10;
      path.lineTo(x, y);
    }

    path.close();

    canvas.drawPath(path, paint);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text(
          'Kindacode.com',
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Column(
          children: [
            CustomPaint(
              painter: _MyPainter(),
            ),
            ElevatedButton(
              onPressed: readJson,
              child: const Text('Load Data'),
            ),

            // Display the data loaded from sample.json
            _items.isNotEmpty
                ? Expanded(
                    child: ListView.builder(
                      itemCount: _items.length,
                      itemBuilder: (context, index) {
                        return Card(
                          key: ValueKey(_items[index]["id"]),
                          margin: const EdgeInsets.all(10),
                          color: Colors.amber.shade100,
                          child: ListTile(
                            leading: Text(_items[index]["id"]),
                            title: Text(_items[index]["name"]),
                            subtitle: Text(_items[index]["description"]),
                          ),
                        );
                      },
                    ),
                  )
                : Container()
          ],
        ),
      ),
    );
  }
}
class _MyPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final _secondFloorState = _SecondFloorState();
    _secondFloorState._drawRectangle(canvas, size);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}