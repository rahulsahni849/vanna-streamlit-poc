def CustomTraining(vn):
    pass

# def CustomTraining(vn):
#     # The information schema query may need some tweaking depending on your database. This is a good starting point.
    
#     df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

#     # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
#     plan = vn.get_training_plan_generic(df_information_schema)

#     # CRC Table: CALGEM_WELL_LIST_T 
#     vn.train(ddl='''
#         SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[CALGEM_PERMITS_T](
# 	[FORM_ID] [int] NOT NULL,
# 	[DISTRICT] [varchar](8) NULL,
# 	[NOTICE_TYPE] [varchar](10) NULL,
# 	[OPERATOR] [varchar](91) NULL,
# 	[API] [varchar](10) NULL,
# 	[WELL_DESIGNATION] [varchar](255) NULL,
# 	[WELL_TYPE] [varchar](20) NULL,
# 	[FIELD] [varchar](255) NULL,
# 	[PLSS] [varchar](16) NULL,
# 	[FORM_STATUS] [varchar](9) NULL,
# 	[COUNTY] [varchar](22) NULL,
# 	[LEASE] [varchar](30) NULL,
# 	[UGS_PROJECT] [varchar](18) NULL,
# 	[CONFIDENTIALITY_REQUESTED] [varchar](3) NULL,
# 	[SUBMITTED_DATE] [date] NULL,
# 	[PERMITTED_DATE] [date] NULL,
# 	[LAST_UPDATED_BY] [varchar](20) NULL,
# 	[LAST_UPDATED_DATE] [datetime] NULL,
# 	[CREATED_BY] [varchar](20) NULL,
# 	[CREATED_BY_DATE] [date] NULL,
# 	[PERMIT_EXP] [date] NULL,
# 	[PERMIT_NO] [int] NULL,
# 	[PERMIT_LINK] [varchar](1000) NULL,
# 	[COMMENTS] [varchar](4000) NULL,
# 	[COMMENTS_DATE] [date] NULL,
# 	[INITIAL_SUB_DATE] [date] NULL,
# 	[EVENT_YORN] [varchar](20) NULL,
# 	[EVENT_DATE] [date] NULL,
# 	[DAY_UNTIL_PERMIT] [int] NULL,
# 	[STATUS_DATE] [date] NULL,
# 	[HISTORY_DUE] [date] NULL,
# 	[HISTORY_SUBMITTED_DATE] [date] NULL,
# 	[RIG_RELEASE] [date] NULL,
# 	[PRIORITY] [int] NULL,
# 	[ENGINEER] [varchar](200) NULL,
# 	[FAULT_BLOCK] [varchar](20) NULL,
# 	[DATE_REQUIRED] [date] NULL,
# 	[CONDUCTOR_SET_DATE] [date] NULL,
# 	[EST_PERMIT_EXP] [date] NULL,
# 	[EXP_YN] [varchar](20) NULL,
# 	[APPROV_QTR] [int] NULL,
# 	[OTHER_TYPE] [varchar](20) NULL
# ) ON [PRIMARY]
# GO
# ALTER TABLE [dbo].[CALGEM_PERMITS_T] ADD PRIMARY KEY CLUSTERED 
# (
# 	[FORM_ID] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
# GO
# CREATE NONCLUSTERED INDEX [NC_IDX_CALGEM_PERMITS_T] ON [dbo].[CALGEM_PERMITS_T]
# (
# 	[SUBMITTED_DATE] ASC,
# 	[PERMITTED_DATE] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
# GO
#             ''')
    
#     vn.train(sql='''
#              SELECT TOP (1000) [FORM_ID]
#       ,[DISTRICT]
#       ,[NOTICE_TYPE]
#       ,[OPERATOR]
#       ,[API]
#       ,[WELL_DESIGNATION]
#       ,[WELL_TYPE]
#       ,[FIELD]
#       ,[PLSS]
#       ,[FORM_STATUS]
#       ,[COUNTY]
#       ,[LEASE]
#       ,[UGS_PROJECT]
#       ,[CONFIDENTIALITY_REQUESTED]
#       ,[SUBMITTED_DATE]
#       ,[PERMITTED_DATE]
#       ,[LAST_UPDATED_BY]
#       ,[LAST_UPDATED_DATE]
#       ,[CREATED_BY]
#       ,[CREATED_BY_DATE]
#       ,[PERMIT_EXP]
#       ,[PERMIT_NO]
#       ,[PERMIT_LINK]
#       ,[COMMENTS]
#       ,[COMMENTS_DATE]
#       ,[INITIAL_SUB_DATE]
#       ,[EVENT_YORN]
#       ,[EVENT_DATE]
#       ,[DAY_UNTIL_PERMIT]
#       ,[STATUS_DATE]
#       ,[HISTORY_DUE]
#       ,[HISTORY_SUBMITTED_DATE]
#       ,[RIG_RELEASE]
#       ,[PRIORITY]
#       ,[ENGINEER]
#       ,[FAULT_BLOCK]
#       ,[DATE_REQUIRED]
#       ,[CONDUCTOR_SET_DATE]
#       ,[EST_PERMIT_EXP]
#       ,[EXP_YN]
#       ,[APPROV_QTR]
#       ,[OTHER_TYPE]
#   FROM [CRC].[dbo].[CALGEM_PERMITS_T]
#             ''')
    
#     # CRC Table: CALGEM_PERMIT_REVIEW_T 
#     vn.train(ddl='''
#         SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[CALGEM_PERMIT_REVIEW_T](
# 	[ID] [int] NULL,
# 	[COMMENTS] [nvarchar](max) NULL,
# 	[COMMENT_DATE] [date] NULL,
# 	[COMMENTER] [nvarchar](255) NULL,
# 	[API_10] [nvarchar](255) NULL,
# 	[STATUS] [nvarchar](255) NULL,
# 	[FORM_ID] [int] NULL,
# 	[last_updated_ts] [datetime] NULL
# ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
# GO
#             ''')
    
#     vn.train(sql='''
#              SELECT TOP (1000) [ID]
#       ,[COMMENTS]
#       ,[COMMENT_DATE]
#       ,[COMMENTER]
#       ,[API_10]
#       ,[STATUS]
#       ,[FORM_ID]
#       ,[last_updated_ts]
#   FROM [CRC].[dbo].[CALGEM_PERMIT_REVIEW_T]
             
#             ''')
    
    
#     # CRC Table: CALGEM_PERMIT_STATUS_T 
#     vn.train(ddl='''
#         SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[CALGEM_PERMIT_STATUS_T](
# 	[REC_ID] [int] NULL,
# 	[FORM_ID] [int] NULL,
# 	[FORM_STATUS] [varchar](20) NULL,
# 	[STATUS_DATE] [date] NULL
# ) ON [PRIMARY]
# GO

#             ''')
    
#     vn.train(sql='''
#              SELECT TOP (1000) [REC_ID]
#       ,[FORM_ID]
#       ,[FORM_STATUS]
#       ,[STATUS_DATE]
#   FROM [CRC].[dbo].[CALGEM_PERMIT_STATUS_T]
#             ''')
    
    
#     # CRC Table: CALGEM_WELL_LIST_T 
#     vn.train(ddl='''
#         SET ANSI_NULLS ON
# GO
# SET QUOTED_IDENTIFIER ON
# GO
# CREATE TABLE [dbo].[CALGEM_WELL_LIST_T](
# 	[API] [varchar](10) NULL,
# 	[DESIGNATION] [varchar](220) NULL,
# 	[OP_NAME] [varchar](180) NULL,
# 	[OP_CODE] [varchar](50) NULL,
# 	[WELL_TYPE] [varchar](140) NULL,
# 	[CALGEM_STATUS] [varchar](60) NULL,
# 	[FIELD_NAME] [varchar](210) NULL,
# 	[LEASE_NAME] [varchar](160) NULL,
# 	[WELL_NO] [varchar](60) NULL,
# 	[DISTRICT] [varchar](60) NULL,
# 	[SEC] [varchar](20) NULL,
# 	[TWN] [varchar](40) NULL,
# 	[RGE] [varchar](40) NULL,
# 	[BM] [varchar](30) NULL,
# 	[LAT] [varchar](110) NULL,
# 	[LONGITUDE] [varchar](120) NULL,
# 	[AREA] [varchar](80) NULL,
# 	[COUNTY] [varchar](40) NULL,
# 	[SPUD_DATE] [varchar](100) NULL,
# 	[CONF_STATUS] [varchar](80) NULL,
# 	[CONF_EXP_DATE] [varchar](100) NULL,
# 	[STATUS_DATE] [varchar](90) NULL,
# 	[NEXT_TEST_DUE] [varchar](100) NULL,
# 	[WELL_STIM] [varchar](50) NULL,
# 	[WELL_MAIN] [varchar](50) NULL
# ) ON [PRIMARY]
# GO

#             ''')
    
#     vn.train(sql='''
#              SELECT TOP (1000) [API]
#       ,[DESIGNATION]
#       ,[OP_NAME]
#       ,[OP_CODE]
#       ,[WELL_TYPE]
#       ,[CALGEM_STATUS]
#       ,[FIELD_NAME]
#       ,[LEASE_NAME]
#       ,[WELL_NO]
#       ,[DISTRICT]
#       ,[SEC]
#       ,[TWN]
#       ,[RGE]
#       ,[BM]
#       ,[LAT]
#       ,[LONGITUDE]
#       ,[AREA]
#       ,[COUNTY]
#       ,[SPUD_DATE]
#       ,[CONF_STATUS]
#       ,[CONF_EXP_DATE]
#       ,[STATUS_DATE]
#       ,[NEXT_TEST_DUE]
#       ,[WELL_STIM]
#       ,[WELL_MAIN]
#   FROM [CRC].[dbo].[CALGEM_WELL_LIST_T]
#             ''')
