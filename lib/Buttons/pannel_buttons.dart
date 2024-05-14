import 'dart:async';
import 'package:flutter/material.dart';
import 'package:semi_controll/parameter.dart';

class ButtonDoor extends StatefulWidget {
  const ButtonDoor({
    super.key,
    required this.inState,
    required this.sector,
    required this.device,
    required this.label,
    required this.setDevState,
  });

  final String inState;
  final String sector;
  final String device;
  final String label;
  final setDevState;

  @override
  State<ButtonDoor> createState() => _ButtonDoorState();
}

class _ButtonDoorState extends State<ButtonDoor> {
  bool btnEnable = true;

  @override
  Widget build(BuildContext context) {
    String outState = widget.inState;
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
                setState(() {});
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
