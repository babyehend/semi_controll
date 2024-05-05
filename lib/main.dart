import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => parameter(),
      child: MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.grey),
          useMaterial3: true,
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({
    super.key,
    this.title = 'SemiConductor Control Pannel',
  });

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // final String serverAdr =
  //     'C:\\Project\\Dart\\semi_controll\\SemiServer\\app.py';

  // @override
  // void initState() {
  //   initBackEndServer();
  //   super.initState();
  // }

  // void initBackEndServer() async {
  //   await Process.start('python', [serverAdr]); // 예시: 'ls -l' 명령 실행
  // }

  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Scaffold(
      appBar: AppBar(
        backgroundColor: prov_para.bgEnd,
        title: Text(widget.title),
      ),
      body: Container(
        height: MediaQuery.of(context).size.height,
        width: MediaQuery.of(context).size.width,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
            colors: [
              prov_para.bgStart,
              prov_para.bgEnd,
            ],
          ),
        ),
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(10),
            margin:
                const EdgeInsets.only(top: 10, left: 40, right: 40, bottom: 30),
            decoration: BoxDecoration(
              color: prov_para.textClr,
              borderRadius: BorderRadius.circular(20),
            ),
            child: prov_para.pageNow,
          ),
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
