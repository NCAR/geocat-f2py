begin
    dim0 = 2
    dim1 = 3
    mxi = 4
    mxo = 3
    nyo = 2

    ; Set different options
    option_1 = False

    option_2 = True
    option_2@method = 1
    option_2@distmx = 275

	data = todouble(random_normal(1, 2, (/dim0, dim1, mxi/)))   ; Normal distribution data, mean = 1 and std.dev = 2

    ; Set additional data with missing value
	data_msg = data
	data_msg(0,0,1)=-99
    data_msg(1,2,3)=-99
	data_msg@_FillValue = -99   ; Set missing value to -99

	print(data)
	print(data_msg)

    ; Initialize coordinates
	xi = (/1.0, 3.0, 5.0, 7.0/)
	yi = (/2.0, 4.0, 6.0, 8.0/)

	; Initialize output grid coordinates
	xgrid = (/1.5, 2.5, 3.5/)
	ygrid = (/2.2, 7.8/)

	out_1 = triple2grid(xi, yi, data, xgrid, ygrid, option_1)
	out_1_msg = triple2grid(xi, yi, data_msg, xgrid, ygrid, option_1)

	out_2 = triple2grid(xi, yi, data, xgrid, ygrid, option_2)
	out_2_msg = triple2grid(xi, yi, data_msg, xgrid, ygrid, option_2)

	print(out_1)
	print(out_1_msg)
	print(out_2)
	print(out_2_msg)
end
