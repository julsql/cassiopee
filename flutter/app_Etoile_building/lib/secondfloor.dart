import 'dart:convert';
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
