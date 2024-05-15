import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:semi_controll/page_auto.dart';
import 'package:semi_controll/page_exit.dart';
import 'package:semi_controll/page_manual.dart';
import 'package:semi_controll/menu_page.dart';

class parameter with ChangeNotifier {
  final Color bgClr = const Color(0xff345da7); // deep blue
  final Color mainClr = const Color(0xff4bb4de); // sky blue
  final Color mainClr2 = const Color(0xffefdbcb); // ivory
  final Color bgStart = const Color(0xff616e7c);
  final Color bgEnd = const Color(0xffcbd2d9);
  final Color textClr = Colors.white70;
  final IconData manualCtrl = Icons.control_camera;
  final IconData autoPros = Icons.web_stories;
  final IconData exit = Icons.exit_to_app;
  final IconData back = Icons.subdirectory_arrow_left;

  final List<Widget> pages = [
    const MenuPage(),
    const PageManual(),
    const PageAuto(),
    const PageExit(),
  ];

  // Changeable value should be called with
  // full format like Provider.of<parameter>(context).value
  Widget pageNow = MenuPage();

  void pageUpdate(int index) {
    pageNow = pages[index];
    notifyListeners();
  }

  // Dio Parameter Section
  final String autoState = 'AUTO_STATE';
  final String sect1 = 'HMDS';
  final String sect2 = 'SPIN';
  final String sect3 = 'BAKE';
  final String sect4 = 'DEVELOP';
  final String sect5 = 'EXPOSURE';

  final String door = 'DOOR';
  final String temp = 'TEMP';
  final List<String> devices = ['DEV1', 'DEV2', 'DEV3'];
  final List<String> modes = ['SPIN_SPEED', 'HEAT_VALUE'];
  final List<String> steps = [''];

  // parameters that communicating with server
  var dio = Dio(BaseOptions(
    baseUrl: 'http://127.0.0.1:5000/',
    connectTimeout: Duration(seconds: 5),
    receiveTimeout: Duration(seconds: 3),
  ));

  String deviceStateShifter(String state) {
    if (state == 'OPEN') {
      return 'CLOSE';
    } else if (state == 'CLOSE') {
      return 'OPEN';
    } else if (state == 'ON') {
      return 'OFF';
    } else if (state == 'OFF') {
      return 'ON';
    } else {
      return state;
    }
  }

  Future<void> patchData(
    String section,
    String device,
    String change,
  ) async {
    await Dio().patch('http://127.0.0.1:5000/', data: {
      section: {device: change}
    });
  }

  String stateShifter(
    String curState,
    String section,
    String device,
  ) {
    String change = deviceStateShifter(curState);
    patchData(section, device, change);
    // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
    return change;
  }

  Future<void> switchState(bool value) async {
    if (value) {
      await Dio().patch('http://127.0.0.1:5000/', data: {
        autoState: {'AUTO': 'ON'}
      });
    } else {
      await Dio().patch('http://127.0.0.1:5000/', data: {
        autoState: {'AUTO': 'OFF'}
      });
    }
  }

  final ButtonStyle ctrlBTNstyle = ElevatedButton.styleFrom(
    backgroundColor: Color(0xff345da7),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
    ),
    disabledForegroundColor: Color(0xff616e7c),
  );

  final TextStyle ctrlTextStyle = TextStyle(
    fontSize: 18,
    color: Colors.white70,
  );

  final TextStyle stateTextStyle = TextStyle(
    fontSize: 18,
  );
}
