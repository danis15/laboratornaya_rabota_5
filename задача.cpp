#include <iostream>
#include <Windows.h>
#include <math.h>

using namespace std;

POINT mouse;

void send_mouse(int pos_x, int pos_y, DWORD key = 0, int which_xbutton = 0)
{
	if (key == MOUSEEVENTF_ABSOLUTE)
	{
		GetCursorPos(&mouse);
	}
	INPUT input;
	MOUSEINPUT mouse_input;
	input.type = INPUT_MOUSE;
	mouse_input.dx = pos_x - mouse.x;
	mouse_input.dy = pos_y - mouse.y;
	mouse_input.mouseData = which_xbutton;
	mouse_input.dwFlags = key == MOUSEEVENTF_ABSOLUTE ? MOUSEEVENTF_MOVE: key;
	mouse_input.time = 0x0;
	mouse_input.dwExtraInfo = 0x0;
	input.mi = mouse_input;
	SendInput(1, &input, sizeof(input));
	mouse.x = 0;
	mouse.y = 0;
}

void send_key(WORD key, bool on)
{
	INPUT input;
	KEYBDINPUT key_input;
	input.type = INPUT_KEYBOARD;
	key_input.wVk = key;
	key_input.wScan = 0x0;
	key_input.dwFlags = on ? 0x0 : KEYEVENTF_KEYUP;
	key_input.time = 0x0;
	key_input.dwExtraInfo = 0x0;
	input.ki = key_input;
	SendInput(1, &input, sizeof(input));
}

int main()
{
	setlocale(LC_ALL, "Russian");
	int x1, y1, x2, y2, x3, y3, r, g, b, stage = 0;
	static bool disable = false;
	HDC hdc = NULL;
	HINSTANCE GDI = NULL;
	cin >> x1 >> y1;
	cin >> x2 >> y2;
	cin >> r >> g >> b;
	cin >> x3 >> y3;

	GDI = LoadLibraryA("gdi32.dll");
	if (!GDI)
	{
		cout << "Ошибка загрузки библиотеки" << endl;
		system("pause");
		return 0;
	}

	while (true)
	{
		float tick = (float)GetTickCount() / 1000.f;
		static auto st_tick = tick;

		switch (stage)
		{
		case 0:
		{
			hdc = GetDC(NULL);
			for (int i = 0; i <= (x2 - x1); i++)
			{
				for (int j = 0; j <= (y2 - y1); j++)
				{
					COLORREF color = GetPixel(hdc, x1 + i, y1 + j);
					if (GetRValue(color) == r && GetGValue(color) == g && GetBValue(color) == b)
					{
						ReleaseDC(NULL, hdc);
						stage = 1;
						break;
					}
				}
			}
		}
			break;
		case 1:
			if (abs(st_tick - tick) >= 0.3f)
			{
				send_key(0x45, true);
				disable = true;
				st_tick = tick;
				stage = 2;
			}
			break;
		case 2:
			if (disable)
			{
				send_key(0x45, false);
				disable = false;
			}
			if (abs(st_tick - tick) >= 0.3f)
			{
				send_mouse(x3, y3, MOUSEEVENTF_ABSOLUTE);
				send_mouse(0, 0, MOUSEEVENTF_LEFTDOWN);
				st_tick = tick;
				stage = 3;
			}
			break;
		case 3:
			send_mouse(0, 0, MOUSEEVENTF_LEFTUP);
			stage = 0;
			break;
		}
	}
}