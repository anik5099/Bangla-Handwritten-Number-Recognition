import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as https;
import 'package:universal_html/html.dart' as html;

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(const MyApp());
}

TextStyle text_style(
    {Color? text_color, double? size, FontWeight? weight = FontWeight.normal}) {
  return TextStyle(
      color: text_color,
      fontSize: size,
      fontWeight: weight,
      fontFamily: 'Lexend');
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  var selectedimage;
  var modelResult = 'No Image is uploaded';
  List<Image> images = [];

  get http => null;
  Future<XFile> pickImage() async {
    ImagePicker picker = ImagePicker();
    XFile? image = await picker.pickImage(source: ImageSource.gallery);
    return XFile(
      image!.path,
    );
  }

  Future<void> uploadImage(XFile image) async {
    var imageBytes = await image.readAsBytes();

    var request = https.MultipartRequest(
        'POST', Uri.parse('http://127.0.0.1:5000/preprocessing'));
    request.files.add(https.MultipartFile.fromBytes('image', imageBytes,
        filename: image.path));

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var jsonResponse = await response.stream.bytesToString();
        var data = json.decode(jsonResponse);

        for (var i in data['images']) {
          List<int> bytes = base64Decode(i);
          Uint8List uint8List = Uint8List.fromList(bytes);

          setState(() {
            images.add(Image.memory(
              uint8List,
              fit: BoxFit.contain, // Adjust the BoxFit property as needed
            ));
          });
        }
        setState(() {
          modelResult = data['number'][0].toString();
          print(modelResult.runtimeType);
        });
      } else {
        print('Error ${response.statusCode}');
      }
    } catch (error) {
      print('hi  hi');
      print('Error: $error');
    }
    print(images.length);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title:
              Text('Bangla Handwritten Number Recognizer', style: text_style()),
          backgroundColor: Color.fromARGB(255, 220, 26, 71)),
      body: Container(
        child: ListView(
          children: [
            GestureDetector(
              onTap: () async {
                XFile file = await pickImage();
                print(file.path);
                setState(() {
                  selectedimage = file.path;
                });
                uploadImage(file);
                images = [];
                modelResult = 'No Image is uploaded';
              },
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Container(
                    width: MediaQuery.of(context).size.width * .5,
                    height: MediaQuery.of(context).size.height * .5,
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.all(Radius.circular(20)),
                        color:
                            Color.fromARGB(255, 220, 26, 71).withOpacity(.2)),
                    child: Center(
                        child: (selectedimage == null)
                            ? Text(
                                'Upload Image of a Bangla number',
                                style: text_style(),
                              )
                            : Image.network(selectedimage))),
              ),
            ),
            (images != null)
                ? Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Container(
                        height: MediaQuery.of(context).size.height * .2,
                        child: Column(
                          children: [
                            Text('Preprocessed Images', style: text_style()),
                            Row(children: images),
                          ],
                        ),
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.all(Radius.circular(20)),
                            color: Color.fromARGB(255, 220, 26, 71)
                                .withOpacity(.2))),
                  )
                : Container(),
            Container(
              width: MediaQuery.of(context).size.width * .7,
              height: MediaQuery.of(context).size.height * .1,
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(20)),
                  color: Color.fromARGB(255, 220, 26, 71).withOpacity(.2)),
              padding: EdgeInsets.all(10.0),
              child: Center(
                  child: Text(
                modelResult.toString(),
                style: text_style(size: 30),
              )),
            ),
          ],
        ),
      ),
    );
  }
}
