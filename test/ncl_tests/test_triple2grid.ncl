begin
    dim0 = 2
    dim1 = 3
    mxi = 4
    mxo = 3
    nyo = 2

    ; Set different options
    option = True
    option@method = 1    ; Just to show it is already set to 1 as default when option is True
    
    option_method_0 = False
    option_method_0@method = 0    ; Just to show it is already set to 0 as default when option is False

    option_distmx_275 = True
    option_distmx_275@method = 1    ; Just to show it is already set to 1 as default when option is True
    option_distmx_275@distmx = 275

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

	out_expected = triple2grid(xi, yi, data, xgrid, ygrid, option)
	print(out_expected)
	out_expected_msg = triple2grid(xi, yi, data_msg, xgrid, ygrid, option)
	print(out_expected_msg)

	out_expected_method_0 = triple2grid(xi, yi, data, xgrid, ygrid, option_method_0)
	print(out_expected_method_0)
	out_expected_method_0_msg = triple2grid(xi, yi, data_msg, xgrid, ygrid, option_method_0)
	print(out_expected_method_0_msg)

	out_expected_distmx_275 = triple2grid(xi, yi, data, xgrid, ygrid, option_distmx_275)
	print(out_expected_distmx_275)
	out_expected_distmx_275_msg = triple2grid(xi, yi, data_msg, xgrid, ygrid, option_distmx_275)
	print(out_expected_distmx_275_msg)


end
