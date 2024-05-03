import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';
import 'package:semi_controll/Buttons/main_button.dart';

class MenuPage extends StatefulWidget {
  const MenuPage({
    super.key,
  });

  @override
  State<MenuPage> createState() => _MenuPageState();
}

class _MenuPageState extends State<MenuPage> {
  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Flexible(
          flex: 1,
          child: Container(
            alignment: Alignment.center,
            child: const Text(
              'Menu Select',
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        Flexible(
          flex: 2,
          child: SizedBox(
            height: double.infinity,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Flexible(
                  flex: 1,
                  child: MainButton(
                    icon: prov_para.manualCtrl,
                    text: "Manual Control",
                    index: 1,
                  ),
                ),
                Flexible(
                  flex: 1,
                  child: MainButton(
                    icon: prov_para.autoPros,
                    text: "Auto Process",
                    index: 2,
                  ),
                ),
                Flexible(
                  flex: 1,
                  child: MainButton(
                    icon: prov_para.exit,
                    text: "Exit",
                    index: 3,
                  ),
                ),
              ],
            ),
          ),
        ),
        Flexible(
          flex: 1,
          child: Container(),
        ),
      ],
    );
  }
}
