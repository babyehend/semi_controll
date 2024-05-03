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
  const PannelHMDS({
    super.key,
    required this.isVisible,
  });

  final bool isVisible;

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
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          statusHead(
            header: parameter().sect1,
          ),
          Flexible(
            flex: 1,
            child: Visibility(
              visible: widget.isVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                    child: Text(
                      'Door',
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "Oxygen",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
                  ),
                ],
              ),
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Door State : $doorState",
                    style: parameter().stateTextStyle,
                  ),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Humid State : $vibState",
                    style: parameter().stateTextStyle,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class statusHead extends StatelessWidget {
  const statusHead({
    required this.header,
    super.key,
  });

  final String header;

  @override
  Widget build(BuildContext context) {
    return Text(
      header,
      style: TextStyle(
        fontWeight: FontWeight.bold,
      ),
    );
  }
}

class PannelSpin extends StatefulWidget {
  const PannelSpin({
    super.key,
    required this.isVisible,
  });

  final bool isVisible;

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
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          statusHead(
            header: parameter().sect2,
          ),
          Flexible(
            flex: 1,
            child: Visibility(
              visible: widget.isVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                    child: Text(
                      "Door",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "Coating",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
                  ),
                ],
              ),
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Door State : $doorState",
                    style: parameter().stateTextStyle,
                  ),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Coating State : $motorState",
                    style: parameter().stateTextStyle,
                  ),
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
  const PannelBake({
    super.key,
    required this.isVisible,
  });

  final bool isVisible;

  @override
  State<PannelBake> createState() => _PannelBakeState();
}

class _PannelBakeState extends State<PannelBake> {
  String doorState = '';
  String temp = '';
  final _valueList = ['SOFT', 'HARD', 'POSTEX'];
  var _selectedValue = 'SOFT';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect3);
    // Timer.periodic(Duration(seconds: 2), (timer) {
    //   fetchTemp(parameter().sect3);
    // });
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
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          statusHead(
            header: parameter().sect3,
          ),
          Flexible(
            flex: 1,
            child: Visibility(
              visible: widget.isVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                    child: Text(
                      "Door",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
                  ),
                  Container(
                    height: 40,
                    padding: EdgeInsets.symmetric(
                      horizontal: 10,
                    ),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(14),
                      color: parameter().bgClr,
                    ),
                    child: DropdownButton(
                      iconEnabledColor: parameter().textClr,
                      underline: Container(),
                      style: TextStyle(
                        color: parameter().textClr,
                        fontWeight: FontWeight.bold,
                      ),
                      focusColor: parameter().bgClr,
                      dropdownColor: parameter().bgClr,
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
                        setState(
                          () {
                            _selectedValue = value.toString();
                            parameter().stateShifter(
                              _selectedValue,
                              parameter().sect3,
                              parameter().dev1,
                            );
                          },
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Door State : $doorState",
                    style: parameter().stateTextStyle,
                  ),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Temperature : $temp",
                    style: parameter().stateTextStyle,
                  ),
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
  const PannelDevel({
    super.key,
    required this.isVisible,
  });

  final bool isVisible;

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
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          statusHead(
            header: parameter().sect4,
          ),
          Flexible(
            flex: 1,
            child: Visibility(
              visible: widget.isVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                    child: Text(
                      "Door",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "FAN",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "Liquid 1",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "Liquid 2",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
                  ),
                ],
              ),
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
                        child: Text(
                          "Door State : $doorState",
                          style: parameter().stateTextStyle,
                        ),
                      ),
                    ),
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          "Fan State : $motorState1",
                          style: parameter().stateTextStyle,
                        ),
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
                        child: Text(
                          "Liquid 1 State : $motorState2",
                          style: parameter().stateTextStyle,
                        ),
                      ),
                    ),
                    Flexible(
                      flex: 1,
                      child: Container(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          "Liquid 2 State : $motorState3",
                          style: parameter().stateTextStyle,
                        ),
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
  const PannelExpos({
    super.key,
    required this.isVisible,
  });

  final bool isVisible;

  @override
  State<PannelExpos> createState() => _PannelExposState();
}

class _PannelExposState extends State<PannelExpos> {
  String doorState = '';
  String ledState = '';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect5);
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
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          statusHead(
            header: parameter().sect5,
          ),
          Flexible(
            flex: 1,
            child: Visibility(
              visible: widget.isVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
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
                    child: Text(
                      "Door",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
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
                    child: Text(
                      "Light",
                      style: parameter().ctrlTextStyle,
                    ),
                    style: parameter().ctrlBTNstyle,
                  ),
                ],
              ),
            ),
          ),
          Flexible(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Door State : $doorState",
                    style: parameter().stateTextStyle,
                  ),
                ),
                Container(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Light State : $ledState",
                    style: parameter().stateTextStyle,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
