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
