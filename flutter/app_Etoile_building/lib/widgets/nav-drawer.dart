import 'package:flutter/material.dart';
import '../home.dart';
import '../about.dart';
import '../floor.dart';

class NavDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          ListTile(
            leading: Icon(Icons.input),
            title: Text('Welcome page'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const HomePage()),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Ground floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(0)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('First floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(1)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Second floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(2)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Third floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(3)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Fourth floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(4)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.info),
            title: Text('About us'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const AboutUs()),
              ),
            },
          ),
        ],
      ),
    );
  }
}
