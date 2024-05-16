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

class PannelBTN extends StatefulWidget {
  const PannelBTN({
    super.key,
    required this.inState,
    required this.sector,
    required this.device,
    required this.label,
    required this.setDevState,
  });

  final dynamic inState;
  final String sector;
  final String device;
  final String label;
  final setDevState;

  @override
  State<PannelBTN> createState() => _PannelBTNState();
}

class _PannelBTNState extends State<PannelBTN> {
  bool btnEnable = true;

  @override
  Widget build(BuildContext context) {
    dynamic outState = widget.inState;
    return ElevatedButton(
      onPressed: btnEnable
          ? () {
              outState = parameter().stateShifter(
                outState,
                widget.sector,
                widget.device,
              );
              widget.setDevState(outState);
              setState(() {
                btnEnable = false;
              });
              Timer(Duration(seconds: 3), () async {
                btnEnable = await true;
                setState(() {
                  if (parameter().devices.contains(widget.device)) {
                    outState = parameter().stateShifter(
                      outState,
                      widget.sector,
                      widget.device,
                    );
                    widget.setDevState(outState);
                  }
                });
              });
            }
          : null,
      child: Text(
        widget.label,
        style: parameter().ctrlTextStyle,
      ),
      style: parameter().ctrlBTNstyle,
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

  void setDoorState(String index) {
    doorState = index;
    setState(() {});
  }

  void setDev1State(String index) {
    vibState = index;
    setState(() {});
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
                  PannelBTN(
                    inState: doorState,
                    sector: parameter().sect1,
                    device: parameter().door,
                    label: 'Door',
                    setDevState: setDoorState,
                  ),
                  PannelBTN(
                    inState: vibState,
                    sector: parameter().sect1,
                    device: parameter().devices[0],
                    label: 'Oxyzen',
                    setDevState: setDev1State,
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
  final _valueList = ['SLOW', 'MIDDLE', 'FAST'];
  var _selectedValue = 'SLOW';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect2);
  }

  void setDoorState(String index) {
    doorState = index;
    setState(() {});
  }

  void setDev1State(String index) {
    motorState = index;
    setState(() {});
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
                  PannelBTN(
                    inState: doorState,
                    sector: parameter().sect2,
                    device: parameter().door,
                    label: 'Door',
                    setDevState: setDoorState,
                  ),
                  PannelBTN(
                    inState: motorState,
                    sector: parameter().sect2,
                    device: parameter().devices[0],
                    label: 'Coating',
                    setDevState: setDev1State,
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
                              parameter().sect2,
                              parameter().modes[0],
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

  late Timer _timer;

  final _valueList = ['SOFT', 'HARD', 'POSTEX'];
  var _selectedValue = 'SOFT';

  @override
  void initState() {
    super.initState();
    fetchData(parameter().sect3);
    _timer = Timer.periodic(Duration(seconds: 1), (timer) async {
      await fetchTemp(parameter().sect3);
      setState(() {});
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  void setDoorState(String index) {
    doorState = index;
    setState(() {});
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
      temp = response.data[section]['TEMP'];
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
                  PannelBTN(
                    inState: doorState,
                    sector: parameter().sect3,
                    device: parameter().door,
                    label: 'Door',
                    setDevState: setDoorState,
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
                              parameter().modes[1],
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

  void setDoorState(String index) {
    doorState = index;
    setState(() {});
  }

  void setDev1State(String index) {
    motorState1 = index;
    setState(() {});
  }

  void setDev2State(String index) {
    motorState2 = index;
    setState(() {});
  }

  void setDev3State(String index) {
    motorState3 = index;
    setState(() {});
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
                  PannelBTN(
                    inState: doorState,
                    sector: parameter().sect4,
                    device: parameter().door,
                    label: 'Door',
                    setDevState: setDoorState,
                  ),
                  PannelBTN(
                    inState: motorState1,
                    sector: parameter().sect4,
                    device: parameter().devices[0],
                    label: 'FAN',
                    setDevState: setDev1State,
                  ),
                  PannelBTN(
                    inState: motorState2,
                    sector: parameter().sect4,
                    device: parameter().devices[1],
                    label: 'Liquid 1',
                    setDevState: setDev2State,
                  ),
                  PannelBTN(
                    inState: motorState3,
                    sector: parameter().sect4,
                    device: parameter().devices[2],
                    label: 'Liquid 2',
                    setDevState: setDev3State,
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

  void setDoorState(String index) {
    doorState = index;
    setState(() {});
  }

  void setDev1State(String index) {
    ledState = index;
    setState(() {});
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
                  PannelBTN(
                    inState: doorState,
                    sector: parameter().sect5,
                    device: parameter().door,
                    label: 'Door',
                    setDevState: setDoorState,
                  ),
                  PannelBTN(
                    inState: ledState,
                    sector: parameter().sect5,
                    device: parameter().devices[0],
                    label: 'LIGHT',
                    setDevState: setDev1State,
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
