begin
    ny = 2
    mx = 3

	data = random_normal(1, 2, (/ny, mx/))   ; Normal distribution data with ny * mx points, mean = 1 and std.dev = 2

    ; Set additional data with missing value
	data_msg = data
	data_msg(0,1)=-99
    data_msg(1,2)=-99
	data_msg@_FillValue = -99   ; Set missing value to -99

	print(data)
	print(data_msg)

    ; Initialize coordinates
	x = (/1.0, 3.0, 5.0/)
	y = (/2.0, 4.0/)

	out = grid2triple(x, y, data)
	out_msg = grid2triple(x, y, data_msg)

	print(out)
	print(out_msg)
end
