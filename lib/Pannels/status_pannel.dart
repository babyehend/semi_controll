import 'dart:async';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';

class PannelBody extends StatelessWidget {
  const PannelBody({
    super.key,
    required this.child,
  });
  final Widget child;

  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Flexible(
      flex: 1,
      child: Container(
        height: 160,
        padding: EdgeInsets.all(5),
        margin: EdgeInsets.fromLTRB(10, 0, 10, 5),
        child: child,
        decoration: BoxDecoration(
          border: Border.all(
            width: 3,
            color: prov_para.mainClr,
          ),
          borderRadius: BorderRadius.all(
            Radius.circular(10),
          ),
        ),
      ),
    );
  }
}

class PannelHMDS extends StatefulWidget {
  const PannelHMDS({super.key});

  @override
  State<PannelHMDS> createState() => _PannelHMDSState();
}

class _PannelHMDSState extends State<PannelHMDS> {
  String doorState = '';
  String vibState = '';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect1);
  }

  Future<void> fetchData(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
      setState(() {
        doorState = response.data[section]['DOOR'];
        vibState = response.data[section]['DEV1'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return PannelBody(
      child: Column(
        children: [
          Text("HMDS"),
          Flexible(
            flex: 1,
            child: Row(
              children: [
                ElevatedButton(
                  onPressed: () {
                    doorState = parameter().stateShifter(
                      doorState,
                      parameter().sect1,
                      parameter().door,
                    );
                    setState(() {});
                  },
                  child: Text(parameter().door),
                ),
                ElevatedButton(
                  onPressed: () {
                    vibState = parameter().stateShifter(
                      vibState,
                      parameter().sect1,
                      parameter().dev1,
                    );
                    // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
                    setState(() {});
                  },
                  child: Text("Oxygen"),
                ),
              ],
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Door State : $doorState"),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Humid State : $vibState"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class PannelSpin extends StatefulWidget {
  const PannelSpin({super.key});

  @override
  State<PannelSpin> createState() => _PannelSpinState();
}

class _PannelSpinState extends State<PannelSpin> {
  String doorState = '';
  String motorState = '';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect2);
  }

  Future<void> fetchData(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
      setState(() {
        doorState = response.data[section]['DOOR'];
        motorState = response.data[section]['DEV1'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return PannelBody(
      child: Column(
        children: [
          Text("Spin Coating"),
          Flexible(
            flex: 1,
            child: Row(
              children: [
                ElevatedButton(
                  onPressed: () {
                    doorState = parameter().stateShifter(
                      doorState,
                      parameter().sect2,
                      parameter().door,
                    );
                    setState(() {});
                  },
                  child: Text("Door"),
                ),
                ElevatedButton(
                  onPressed: () {
                    motorState = parameter().stateShifter(
                      motorState,
                      parameter().sect2,
                      parameter().dev1,
                    );
                    setState(() {});
                  },
                  child: Text("Coating"),
                ),
              ],
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Door State : $doorState"),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Coating State : $motorState"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class PannelBake extends StatefulWidget {
  const PannelBake({super.key});

  @override
  State<PannelBake> createState() => _PannelBakeState();
}

class _PannelBakeState extends State<PannelBake> {
  Timer? _timer = null;
  String doorState = '';
  String temp = '';
  final _valueList = ['SOFT', 'HARD', 'POSTEX'];
  var _selectedValue = 'SOFT';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect3);
    _timer = Timer.periodic(Duration(microseconds: 500), (timer) {
      fetchTemp(parameter().sect3);
    });
  }

  Future<void> fetchData(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
      setState(() {
        doorState = response.data[section]['DOOR'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  Future<void> fetchTemp(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      setState(() {
        temp = response.data[section]['TEMP'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return PannelBody(
      child: Column(
        children: [
          Text("Bake"),
          Flexible(
            flex: 1,
            child: Row(
              children: [
                ElevatedButton(
                  onPressed: () {
                    doorState = parameter().stateShifter(
                      doorState,
                      parameter().sect3,
                      parameter().door,
                    );
                    setState(() {});
                  },
                  child: Text("Door"),
                ),
                DropdownButton(
                  value: _selectedValue,
                  items: _valueList.map(
                    (value) {
                      return DropdownMenuItem(
                        value: value,
                        child: Text(value),
                      );
                    },
                  ).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedValue = value.toString();
                      parameter().stateShifter(
                        _selectedValue,
                        parameter().sect3,
                        parameter().dev1,
                      );
                    });
                  },
                ),
              ],
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Door State : $doorState"),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Temperature : $temp"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class PannelDevel extends StatefulWidget {
  const PannelDevel({super.key});

  @override
  State<PannelDevel> createState() => _PannelDevelState();
}

class _PannelDevelState extends State<PannelDevel> {
  String doorState = '';
  String motorState1 = '';
  String motorState2 = '';
  String motorState3 = '';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect4);
  }

  Future<void> fetchData(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
      setState(() {
        doorState = response.data[section]['DOOR'];
        motorState1 = response.data[section]['DEV1'];
        motorState2 = response.data[section]['DEV2'];
        motorState3 = response.data[section]['DEV3'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return PannelBody(
      child: Column(
        children: [
          Text("Develop"),
          Flexible(
            flex: 1,
            child: Row(
              children: [
                ElevatedButton(
                  onPressed: () {
                    doorState = parameter().stateShifter(
                      doorState,
                      parameter().sect4,
                      parameter().door,
                    );
                    setState(() {});
                  },
                  child: Text("Door"),
                ),
                ElevatedButton(
                  onPressed: () {
                    motorState1 = parameter().stateShifter(
                      motorState1,
                      parameter().sect4,
                      parameter().dev1,
                    );
                    setState(() {});
                  },
                  child: Text("FAN"),
                ),
                ElevatedButton(
                  onPressed: () {
                    motorState2 = parameter().stateShifter(
                      motorState2,
                      parameter().sect4,
                      parameter().dev2,
                    );
                    setState(() {});
                  },
                  child: Text("Liquid 1"),
                ),
                ElevatedButton(
                  onPressed: () {
                    motorState3 = parameter().stateShifter(
                      motorState3,
                      parameter().sect4,
                      parameter().dev3,
                    );
                    setState(() {});
                  },
                  child: Text("Liquid 2"),
                ),
              ],
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text("Door State : $doorState"),
                      ),
                    ),
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text("Fan State : $motorState1"),
                      ),
                    ),
                  ],
                ),
                Row(
                  children: [
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text("Liquid 1 State : $motorState2"),
                      ),
                    ),
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text("Liquid 2 State : $motorState3"),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class PannelExpos extends StatefulWidget {
  const PannelExpos({super.key});

  @override
  State<PannelExpos> createState() => _PannelExposState();
}

class _PannelExposState extends State<PannelExpos> {
  String doorState = '';
  String ledState = '';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect3);
  }

  Future<void> fetchData(
    String section,
  ) async {
    try {
      final response = await Dio().get('http://127.0.0.1:5000/');
      // 가져온 데이터에서 필요한 값을 추출하여 상태 업데이트
      setState(() {
        doorState = response.data[section]['DOOR'];
        ledState = response.data[section]['DEV1'];
      });
    } catch (error) {
      print('Error fetching data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return PannelBody(
      child: Column(
        children: [
          Text("Exposure"),
          Flexible(
            flex: 1,
            child: Row(
              children: [
                ElevatedButton(
                  onPressed: () {
                    doorState = parameter().stateShifter(
                      doorState,
                      parameter().sect5,
                      parameter().door,
                    );
                    setState(() {});
                  },
                  child: Text("Door"),
                ),
                ElevatedButton(
                  onPressed: () {
                    ledState = parameter().stateShifter(
                      ledState,
                      parameter().sect5,
                      parameter().dev1,
                    );
                    setState(() {});
                  },
                  child: Text("Light"),
                ),
              ],
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Door State : $doorState"),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text("Light State : $ledState"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
