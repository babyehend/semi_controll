import 'Pannels/status_pannel.dart';
import 'package:flutter/material.dart';
import 'package:semi_controll/parameter.dart';
import 'package:semi_controll/Buttons/back_button.dart' as myback;

class PageAuto extends StatefulWidget {
  const PageAuto({super.key});

  @override
  State<PageAuto> createState() => _PageAutoState();
}

class _PageAutoState extends State<PageAuto> {
  bool _isChecked = false;

  @override
  void initState() {
    parameter().switchState(_isChecked);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Flexible(
          flex: 1,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              myback.BackButton(),
              SizedBox(
                width: 120,
              ),
              Text(
                "Auto Process",
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(),
              Container(
                child: Row(
                  children: [
                    Text('Process ON / OFF'),
                    Switch(
                      value: _isChecked,
                      onChanged: (value) {
                        setState(() {
                          parameter().switchState(value);
                          _isChecked = value;
                        });
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        Flexible(
          flex: 4,
          child: SizedBox(
            height: double.infinity,
            child: Column(
              children: [
                Row(
                  children: [
                    PannelHMDS(),
                    PannelSpin(),
                    PannelExpos(),
                  ],
                ),
                Row(
                  children: [
                    PannelDevel(),
                    PannelBake(),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
