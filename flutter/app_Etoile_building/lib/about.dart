import 'package:flutter/material.dart';

// About Us

class AboutUs extends StatelessWidget {
  const AboutUs({super.key});

  @override
  Widget build(BuildContext context) {
    Widget textSection = const Padding(
      padding: EdgeInsets.all(32),
      child: Text(
        'Project made by Juliette Debono, Inès Kacer, Sarah Zakon and Iris Marjollet during the Cassiopee project.',
        softWrap: true,
      ),
    );

    return Scaffold(
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
        ],
      ),
    );
  }
}
